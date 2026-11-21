import io
import zlib
from PIL import Image

# Approximate character widths for Times-Roman (in 1/1000th of em)
# Standard Adobe Type 1 Times-Roman metrics
TIMES_WIDTHS = {
    ' ': 250, '!': 333, '"': 408, '#': 500, '$': 500, '%': 833, '&': 778, "'": 333,
    '(': 333, ')': 333, '*': 500, '+': 564, ',': 250, '-': 333, '.': 250, '/': 278,
    '0': 500, '1': 500, '2': 500, '3': 500, '4': 500, '5': 500, '6': 500, '7': 500,
    '8': 500, '9': 500, ':': 278, ';': 278, '<': 564, '=': 564, '>': 564, '?': 444,
    '@': 921, 'A': 722, 'B': 667, 'C': 667, 'D': 722, 'E': 611, 'F': 556, 'G': 722,
    'H': 722, 'I': 333, 'J': 389, 'K': 722, 'L': 611, 'M': 889, 'N': 722, 'O': 722,
    'P': 556, 'Q': 722, 'R': 667, 'S': 556, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 722, 'Y': 667, 'Z': 611, '[': 333, '\\': 278, ']': 333, '^': 469, '_': 500,
    '`': 333, 'a': 444, 'b': 500, 'c': 444, 'd': 500, 'e': 444, 'f': 278, 'g': 500,
    'h': 500, 'i': 278, 'j': 278, 'k': 444, 'l': 278, 'm': 722, 'n': 500, 'o': 500,
    'p': 500, 'q': 500, 'r': 333, 's': 389, 't': 278, 'u': 500, 'v': 444, 'w': 667,
    'x': 444, 'y': 444, 'z': 389, '{': 348, '|': 220, '}': 348, '~': 520
}

def string_width(text, font_name, size):
    if 'Courier' in font_name:
        return len(text) * size * 0.6
    w = 0
    for char in text:
        w += TIMES_WIDTHS.get(char, 500)
    return (w / 1000.0) * size

class PDFDocument:
    def __init__(self):
        self.objects = []
        self.pages = []
        self.images = {} # name -> obj_id
        self.page_width = 595.28   # A4
        self.page_height = 841.89  # A4
        
        # GEHU Annexure I margins
        self.margin_left = 99.2    # 3.5 cm
        self.margin_top = 70.9     # 2.5 cm
        self.margin_right = 35.4   # 1.25 cm
        self.margin_bottom = 35.4  # 1.25 cm
        self.printable_width = self.page_width - self.margin_left - self.margin_right

        # Font object IDs
        self.fonts = {
            'Times-Roman': None,
            'Times-Bold': None,
            'Times-Italic': None,
            'Times-BoldItalic': None,
            'Courier': None,
            'Courier-Bold': None
        }

    def add_object(self, content):
        self.objects.append(content)
        return len(self.objects)

    def register_image(self, image_path):
        if image_path in self.images:
            return self.images[image_path]

        im = Image.open(image_path)
        im = im.convert('RGB')
        w, h = im.size
        
        # JPEG stream
        buf = io.BytesIO()
        im.save(buf, format='JPEG', quality=85)
        jpeg_data = buf.getvalue()

        obj_data = (
            f"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} "
            f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode "
            f"/Length {len(jpeg_data)} >>\nstream\n"
        ).encode('latin1') + jpeg_data + b"\nendstream"

        img_id = self.add_object(obj_data)
        self.images[image_path] = (f"Im{len(self.images)+1}", img_id)
        return self.images[image_path]

class PageWriter:
    def __init__(self, doc, is_cover=False, is_front_matter=False, page_label=""):
        self.doc = doc
        self.is_cover = is_cover
        self.is_front_matter = is_front_matter
        self.page_label = page_label
        self.stream = []
        self.cursor_y = doc.page_height - doc.margin_top
        self.images_used = {} # alias -> obj_id

    def draw_running_header(self, chapter_title=""):
        if self.is_cover or not self.page_label:
            return
        # Top rule
        y_rule = self.doc.page_height - self.doc.margin_top + 18
        self.stream.append(f"0.5 w 0.3 0.3 0.3 RG {self.doc.margin_left:.2f} {y_rule:.2f} m {self.doc.page_width - self.doc.margin_right:.2f} {y_rule:.2f} l S")
        
        # Header text: chapter on left, page number on right
        self.stream.append("BT /Times-Italic 9.5 Tf 0.3 0.3 0.3 rg")
        if chapter_title:
            self.stream.append(f"{self.doc.margin_left:.2f} {y_rule + 4:.2f} Td ({self.escape(chapter_title)}) Tj")
        self.stream.append("ET")

        self.stream.append("BT /Times-Bold 10 Tf 0 0 0 rg")
        p_w = string_width(str(self.page_label), 'Times-Bold', 10)
        x_pos = self.doc.page_width - self.doc.margin_right - p_w
        self.stream.append(f"{x_pos:.2f} {y_rule + 4:.2f} Td ({self.page_label}) Tj ET")

    def escape(self, text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    def draw_text(self, x, y, text, font='Times-Roman', size=12, color=(0,0,0)):
        r, g, b = color
        self.stream.append(f"BT /{font} {size} Tf {r:.2f} {g:.2f} {b:.2f} rg {x:.2f} {y:.2f} Td ({self.escape(text)}) Tj ET")

    def draw_text_centered(self, y, text, font='Times-Bold', size=14, color=(0,0,0)):
        w = string_width(text, font, size)
        x = (self.doc.page_width - w) / 2.0
        self.draw_text(x, y, text, font, size, color)

    def draw_image(self, image_path, x, y, w, h):
        alias, img_id = self.doc.register_image(image_path)
        self.images_used[alias] = img_id
        self.stream.append(f"q {w:.2f} 0 0 {h:.2f} {x:.2f} {y:.2f} cm /{alias} Do Q")

    def draw_rect(self, x, y, w, h, fill_color=None, border_color=(0.2,0.2,0.2), line_width=1):
        if fill_color:
            r, g, b = fill_color
            self.stream.append(f"{r:.2f} {g:.2f} {b:.2f} rg {x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")
        if border_color:
            r, g, b = border_color
            self.stream.append(f"{line_width:.2f} w {r:.2f} {g:.2f} {b:.2f} RG {x:.2f} {y:.2f} {w:.2f} {h:.2f} re S")

    def get_content_stream(self):
        return "\n".join(self.stream).encode('latin1')
