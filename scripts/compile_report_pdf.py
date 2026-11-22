import os
import subprocess
import re
import html
import pypdf

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_HTML = r"D:\Mini5th\report\compiled\report.html"
TEMP_PASS1_PDF = r"D:\Mini5th\report\compiled\report_pass1.pdf"
TEMP_PASS2_PDF = r"D:\Mini5th\report\compiled\report_pass2.pdf"
OVERLAY_HTML = r"D:\Mini5th\report\compiled\overlay.html"
OVERLAY_PDF = r"D:\Mini5th\report\compiled\overlay.pdf"
OUTPUT_PDF = r"D:\Mini5th\StayMart_Project_Report.pdf"

print("Building complete academic report document conforming strictly to GEHU specifications (80 Pages)...")

chapters = {}
for ch in range(1, 10):
    files = [f for f in os.listdir("report/chapters") if f.startswith(f"ch{ch}_")]
    if files:
        with open(os.path.join("report/chapters", files[0]), 'r', encoding='utf-8') as f:
            chapters[ch] = f.read()

appendices = {}
for app in ["app_api_specs.tex", "app_database_schema.tex"]:
    if os.path.exists(os.path.join("report/appendices", app)):
        with open(os.path.join("report/appendices", app), 'r', encoding='utf-8') as f:
            appendices[app] = f.read()

print(f"Loaded {len(chapters)} chapters.")

def to_roman(n):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i"]
    roman_num = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

def extract_latex_command_arg(text, start_idx):
    if start_idx >= len(text) or text[start_idx] != '{':
        return None, start_idx
    depth = 0
    for i in range(start_idx, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start_idx + 1:i], i + 1
    return None, start_idx

def replace_command_balanced(text, cmd_name, template_fn):
    prefix = f'\\{cmd_name}'
    pos = 0
    result = []
    while True:
        idx = text.find(prefix, pos)
        if idx == -1:
            result.append(text[pos:])
            break
        cur = idx + len(prefix)
        while cur < len(text) and text[cur] in ' \t':
            cur += 1
        if cur < len(text) and text[cur] == '{':
            result.append(text[pos:idx])
            inner, end_idx = extract_latex_command_arg(text, cur)
            if inner is not None:
                result.append(template_fn(inner))
                pos = end_idx
            else:
                result.append(text[idx:cur+1])
                pos = cur + 1
        else:
            result.append(text[pos:idx + len(prefix)])
            pos = idx + len(prefix)
    return ''.join(result)

REF_MAP = {
    'tab:comparative_matrix': '2.1',
    'tab:functional_reqs': '3.1',
    'tab:environment_specs': '3.2',
    'tab:dict_users': '4.1',
    'tab:dict_locations': '4.2',
    'tab:dict_categories': '4.3',
    'tab:dict_properties': '4.4',
    'tab:dict_rooms': '4.5',
    'tab:dict_products': '4.6',
    'tab:test_execution_matrix': '7.1',
    'fig:high_level_arch': '1.1',
    'fig:framework_overview': '1.1',
    'fig:microservice_topology': '2.1',
    'fig:deployment_topology': '2.1',
    'fig:dfd_level0': '3.1',
    'fig:dfd0': '3.1',
    'fig:seq_booking': '3.2',
    'fig:erd_model': '4.1',
    'fig:swagger_ui': '5.1',
    'fig:swagger_api': '5.1',
    'fig:ml_pipeline': '5.2',
    'fig:landing_page_ui': '6.1',
    'fig:walkthrough_landing': '6.1',
    'fig:auth_screens': '6.2',
    'fig:search_screens': '6.3',
    'fig:detail_screens': '6.4',
    'fig:post_screens': '6.5',
    'fig:user_dashboard_ui': '6.6',
    'fig:user_portal_screens': '6.6',
    'fig:chat_ui': '6.6',
    'fig:admin_dashboard_ui': '6.7',
    'fig:admin_management_screens': '6.7',
    'fig:walkthrough_search': '7.1',
    'fig:walkthrough_detail': '7.2',
    'fig:walkthrough_product_screens': '7.3',
    'fig:walkthrough_chat': '7.4',
    'fig:walkthrough_admin': '7.5',
    'fig:walkthrough_bookings': '7.6',
    'fig:cloud_topology': '8.1',
    'lst:dockerfile_backend': '8.1',
    'lst:dockerfile_ml': '8.2',
    'lst:docker_compose': '8.3',
    'lst:github_actions': '8.4',
}

def clean_inline_latex(text):
    text = replace_command_balanced(text, 'textbf', lambda c: f'<strong>{c}</strong>')
    text = replace_command_balanced(text, 'textit', lambda c: f'<em>{c}</em>')
    text = replace_command_balanced(text, 'emph', lambda c: f'<em>{c}</em>')
    text = replace_command_balanced(text, 'underline', lambda c: f'<u>{c}</u>')
    def repl_tt(code):
        code = code.replace(r'\_', '_')
        return f'<code>{html.escape(code)}</code>'
    text = replace_command_balanced(text, 'texttt', repl_tt)
    text = replace_command_balanced(text, 'cite', lambda c: f'[{c}]')
    text = replace_command_balanced(text, 'ref', lambda c: REF_MAP.get(c, c.split(':', 1)[-1]))
    text = replace_command_balanced(text, 'label', lambda c: '')
    text = text.replace(r'\$', '$')
    text = text.replace(r'\%', '%')
    text = text.replace(r'\_', '_')
    text = text.replace(r'\&', '&amp;')
    text = text.replace(r'\rightarrow', '&rarr;')
    text = text.replace(r'\times', '&times;')
    text = text.replace('``', '&ldquo;').replace("''", '&rdquo;')
    text = text.replace('---', '&mdash;').replace('--', '&ndash;')
    def repl_math(m):
        m_content = m.group(1).strip()
        m_content = m_content.replace(r'\rightarrow', '&rarr;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<em>{m_content}</em>'
    text = re.sub(r'\$([^\$\n]+)\$', repl_math, text)
    return text.strip()

def parse_latex_table(table_raw, ch_num=None, table_index=1):
    cap_match = re.search(r'\\caption\{', table_raw)
    caption_text = ""
    if cap_match:
        start_brace = cap_match.end() - 1
        cap_inner, _ = extract_latex_command_arg(table_raw, start_brace)
        if cap_inner:
            caption_text = clean_inline_latex(cap_inner)
    
    marker_str = ""
    if caption_text:
        if ch_num is not None:
            table_label = f"Table {ch_num}.{table_index}"
            marker_str = f'<span class="page-marker">[[LOC:TAB_{ch_num}_{table_index}]]</span>'
            if not caption_text.lower().startswith("table"):
                caption_text = f"{marker_str}<strong>{table_label}:</strong> {caption_text}"
            else:
                caption_text = f"{marker_str}<strong>{caption_text}</strong>"
        elif not caption_text.lower().startswith("table"):
            caption_text = f"<strong>Table {table_index}:</strong> {caption_text}"

    if r'\toprule' in table_raw:
        rows_start = table_raw.find(r'\toprule') + len(r'\toprule')
    else:
        m_tab = re.search(r'\\begin\{(?:tabularx|tabular)\}[^\n]*\n', table_raw)
        rows_start = m_tab.end() if m_tab else 0
        
    if r'\bottomrule' in table_raw:
        rows_end = table_raw.find(r'\bottomrule', rows_start)
    else:
        m_end = re.search(r'\\end\{(?:tabularx|tabular)\}', table_raw)
        rows_end = m_end.start() if m_end else len(table_raw)

    tab_content = table_raw[rows_start:rows_end].strip()

    if r'\midrule' in tab_content:
        header_part, body_part = tab_content.split(r'\midrule', 1)
    else:
        header_part = ""
        body_part = tab_content

    rowspan_skips = {}

    def parse_rows(section_text, is_header=False):
        cleaned = re.sub(r'\\(?:toprule|bottomrule|midrule|hline|footnotesize|centering|small)', '', section_text)
        raw_rows = re.split(r'\\\\\s*(?:\[[^\]]*\])?', cleaned)
        parsed_rows = []
        
        for r in raw_rows:
            r = r.strip()
            if not r:
                continue
            raw_cells = re.split(r'(?<!\\)&', r)
            row_html_cells = []
            col_idx = 0
            
            for cell in raw_cells:
                if col_idx in rowspan_skips and rowspan_skips[col_idx] > 0 and not cell.strip():
                    rowspan_skips[col_idx] -= 1
                    col_idx += 1
                    continue

                cell_str = cell.strip()
                multirow_match = re.search(r'\\multirow\{(\d+)\}(?:\{[^\}]*\})?\{', cell_str)
                rowspan_attr = ""
                if multirow_match:
                    num_rows = int(multirow_match.group(1))
                    start_pos = multirow_match.end() - 1
                    inner_content, end_pos = extract_latex_command_arg(cell_str, start_pos)
                    if inner_content is not None:
                        cell_str = cell_str[:multirow_match.start()] + inner_content + cell_str[end_pos:]
                        rowspan_attr = f' rowspan="{num_rows}"'
                        if num_rows > 1:
                            rowspan_skips[col_idx] = num_rows - 1

                multicolumn_match = re.search(r'\\multicolumn\{(\d+)\}(?:\{[^\}]*\})?\{', cell_str)
                colspan_attr = ""
                if multicolumn_match:
                    num_cols = int(multicolumn_match.group(1))
                    start_pos = multicolumn_match.end() - 1
                    inner_content, end_pos = extract_latex_command_arg(cell_str, start_pos)
                    if inner_content is not None:
                        cell_str = cell_str[:multicolumn_match.start()] + inner_content + cell_str[end_pos:]
                        colspan_attr = f' colspan="{num_cols}"'

                formatted_cell = clean_inline_latex(cell_str)
                tag = "th" if is_header else "td"
                row_html_cells.append(f'<{tag}{rowspan_attr}{colspan_attr}>{formatted_cell}</{tag}>')
                col_idx += 1
            
            if row_html_cells:
                inner_tr = "".join(row_html_cells)
                parsed_rows.append(f"<tr>{inner_tr}</tr>")
        return parsed_rows

    header_rows = parse_rows(header_part, is_header=True) if header_part.strip() else []
    body_rows = parse_rows(body_part, is_header=False)
    
    html_out = ['<div class="table-container">']
    if caption_text:
        html_out.append(f'  <div class="table-caption">{caption_text}</div>')
    html_out.append('  <table>')
    if header_rows:
        html_out.append('    <thead>')
        for hr in header_rows:
            html_out.append(f'      {hr}')
        html_out.append('    </thead>')
    if body_rows:
        html_out.append('    <tbody>')
        for br in body_rows:
            html_out.append(f'      {br}')
        html_out.append('    </tbody>')
    html_out.append('  </table>')
    html_out.append('</div>')
    return '\n'.join(html_out)

def latex_to_html_content(tex, ch_num=None, app_letter=None):
    blocks = {}
    block_counter = 0

    table_counter = 1
    def replace_table_match(m):
        nonlocal block_counter, table_counter
        html_tbl = parse_latex_table(m.group(0), ch_num=ch_num, table_index=table_counter)
        table_counter += 1
        key = f"___BLOCK_PLACEHOLDER_{block_counter}___"
        block_counter += 1
        blocks[key] = html_tbl
        return f"\n\n{key}\n\n"

    tex = re.sub(r'\\begin\{table\}(?:\[[^\]]*\])?[\s\S]*?\\end\{table\}', replace_table_match, tex)

    fig_counter = 1
    def replace_fig(m):
        nonlocal block_counter, fig_counter
        caption_match = re.search(r'\\caption\{', m.group(0))
        cap = ""
        if caption_match:
            cap_inner, _ = extract_latex_command_arg(m.group(0), caption_match.end() - 1)
            if cap_inner:
                cap = clean_inline_latex(cap_inner)

        if ch_num is not None:
            f_label = f"Figure {ch_num}.{fig_counter}"
            marker_str = f'<span class="page-marker">[[LOC:FIG_{ch_num}_{fig_counter}]]</span>'
            fig_counter += 1
        else:
            f_label = "Figure"
            marker_str = ""

        if cap.lower().startswith("figure"):
            caption_html = f'{marker_str}<strong>{cap}</strong>'
        elif cap:
            caption_html = f'{marker_str}<strong>{f_label}:</strong> {cap}'
        else:
            caption_html = f'{marker_str}'

        img_match = re.search(r'\\includegraphics\[.*?\]\{([^}]+)\}', m.group(0))
        subfigs = re.findall(r'\\begin\{subfigure\}[\s\S]*?\\includegraphics\[.*?\]\{([^}]+)\}[\s\S]*?\\caption\{([^}]+)\}[\s\S]*?\\end\{subfigure\}', m.group(0))
        
        ch_class = f" fig-ch{ch_num}" if ch_num is not None else ""
        if subfigs:
            html_fig = f'<div class="figure-container{ch_class}"><div class="subfig-row">'
            for img, sub_cap in subfigs:
                img_path = img.replace('\\', '/')
                if not img_path.startswith('http') and not os.path.isabs(img_path):
                    if os.path.exists(os.path.join("report", img_path)):
                        img_path = f"file:///D:/Mini5th/report/{img_path}"
                    elif os.path.exists(img_path):
                        img_path = f"file:///D:/Mini5th/{img_path}"
                    else:
                        img_path = f"file:///D:/Mini5th/{img_path}"
                clean_sub_cap = clean_inline_latex(sub_cap)
                html_fig += f'<div class="subfig"><img src="{img_path}" alt="{clean_sub_cap}"><div class="subfig-cap">({clean_sub_cap})</div></div>'
            html_fig += '</div>'
            if caption_html:
                html_fig += f'<div class="figure-caption">{caption_html}</div>'
            html_fig += '</div>'
            key = f"___BLOCK_PLACEHOLDER_{block_counter}___"
            block_counter += 1
            blocks[key] = html_fig
            return f"\n\n{key}\n\n"

        if img_match:
            img = img_match.group(1).replace('\\', '/')
            if not img.startswith('http') and not os.path.isabs(img):
                if os.path.exists(os.path.join("report", img)):
                    img = f"file:///D:/Mini5th/report/{img}"
                elif os.path.exists(img):
                    img = f"file:///D:/Mini5th/{img}"
            html_fig = f'<div class="figure-container{ch_class}"><img src="{img}" alt="{cap}"><div class="figure-caption">{caption_html}</div></div>'
            key = f"___BLOCK_PLACEHOLDER_{block_counter}___"
            block_counter += 1
            blocks[key] = html_fig
            return f"\n\n{key}\n\n"
        return ''

    tex = re.sub(r'\\begin\{figure\}[\s\S]*?\\end\{figure\}', replace_fig, tex)

    parts = []
    curr = tex
    while '\\begin{lstlisting}' in curr:
        b_idx = curr.find('\\begin{lstlisting}')
        parts.append(curr[:b_idx])
        opt_end = curr.find('\n', b_idx)
        e_idx = curr.find('\\end{lstlisting}', opt_end)
        if e_idx == -1:
            parts.append(curr[b_idx:])
            curr = ""
            break
        raw_code = curr[opt_end+1:e_idx]
        key = f"___BLOCK_PLACEHOLDER_{block_counter}___"
        block_counter += 1
        blocks[key] = f'<div class="code-container"><pre>{html.escape(raw_code.strip())}</pre></div>'
        parts.append(f"\n\n{key}\n\n")
        curr = curr[e_idx + len('\\end{lstlisting}'):]
    parts.append(curr)
    tex = "".join(parts)

    lines = tex.splitlines()
    html_lines = []
    in_itemize = False
    in_enumerate = False
    para_acc = []
    sec_counter = 1
    subsec_counter = 1

    def flush_para():
        nonlocal para_acc
        if para_acc:
            raw_p = " ".join(para_acc).strip()
            para_acc = []
            if raw_p:
                if raw_p in blocks:
                    html_lines.append(blocks[raw_p])
                else:
                    for k, v in blocks.items():
                        if k in raw_p:
                            raw_p = raw_p.replace(k, v)
                    cleaned = clean_inline_latex(raw_p)
                    if cleaned.startswith('<div') or cleaned.startswith('<table'):
                        html_lines.append(cleaned)
                    else:
                        html_lines.append(f'<p>{cleaned}</p>')

    for line in lines:
        sline = line.strip()

        if sline.startswith(r'\chapter{'):
            flush_para()
            t_match = re.search(r'\\chapter\{([^}]+)\}', sline)
            title = t_match.group(1) if t_match else "Chapter"
            clean_title = clean_inline_latex(title)
            if ch_num is not None:
                html_lines.append(f'<span class="page-marker">[[LOC:CH_{ch_num}]]</span><h1 class="chapter-title">Chapter {ch_num}<br>{clean_title}</h1>')
            elif app_letter is not None:
                html_lines.append(f'<span class="page-marker">[[LOC:APP_{app_letter}]]</span><h1 class="chapter-title">Appendix {app_letter}<br>{clean_title}</h1>')
            else:
                html_lines.append(f'<h1 class="chapter-title">{clean_title}</h1>')
            sec_counter = 1
            continue

        if sline.startswith(r'\section{'):
            flush_para()
            t_match = re.search(r'\\section\{([^}]+)\}', sline)
            title = t_match.group(1) if t_match else "Section"
            clean_title = clean_inline_latex(title)
            if ch_num is not None:
                html_lines.append(f'<span class="page-marker">[[LOC:SEC_{ch_num}_{sec_counter}]]</span><h2 class="section-title">{ch_num}.{sec_counter} {clean_title}</h2>')
                sec_counter += 1
            elif app_letter is not None:
                html_lines.append(f'<h2 class="section-title">{app_letter}.{sec_counter} {clean_title}</h2>')
                sec_counter += 1
            else:
                html_lines.append(f'<h2 class="section-title">{clean_title}</h2>')
            subsec_counter = 1
            continue

        if sline.startswith(r'\subsection{'):
            flush_para()
            t_match = re.search(r'\\subsection\{([^}]+)\}', sline)
            title = t_match.group(1) if t_match else "Subsection"
            clean_title = clean_inline_latex(title)
            if ch_num is not None:
                cur_sec = max(1, sec_counter - 1)
                html_lines.append(f'<h3 class="subsection-title">{ch_num}.{cur_sec}.{subsec_counter} {clean_title}</h3>')
                subsec_counter += 1
            else:
                html_lines.append(f'<h3 class="subsection-title">{clean_title}</h3>')
            continue

        if sline.startswith(r'\subsubsection{'):
            flush_para()
            t_match = re.search(r'\\subsubsection\{([^}]+)\}', sline)
            title = t_match.group(1) if t_match else "Subsubsection"
            clean_title = clean_inline_latex(title)
            html_lines.append(f'<h4 class="subsubsection-title">{clean_title}</h4>')
            continue

        if r'\begin{itemize}' in sline:
            flush_para()
            html_lines.append('<ul>')
            in_itemize = True
            continue

        if r'\end{itemize}' in sline:
            flush_para()
            html_lines.append('</ul>')
            in_itemize = False
            continue

        if r'\begin{enumerate}' in sline:
            flush_para()
            html_lines.append('<ol>')
            in_enumerate = True
            continue

        if r'\end{enumerate}' in sline:
            flush_para()
            html_lines.append('</ol>')
            in_enumerate = False
            continue

        if sline.startswith(r'\item'):
            flush_para()
            content = sline[5:].strip()
            for k, v in blocks.items():
                if k in content:
                    content = content.replace(k, v)
            html_lines.append(f'<li>{clean_inline_latex(content)}</li>')
            continue

        if not sline or sline.startswith('%'):
            flush_para()
            continue

        para_acc.append(sline)

    flush_para()
    return '\n'.join(html_lines)

TOC_DEFINITIONS = [
    ("prelim", "Abstract", "[[LOC:ABSTRACT]]", 0),
    ("prelim", "Acknowledgements", "[[LOC:ACKNOWLEDGEMENTS]]", 0),
    ("prelim", "Contents", "[[LOC:TOC]]", 0),
    ("prelim", "List of Abbreviations", "[[LOC:LOA]]", 0),
    ("prelim", "List of Figures", "[[LOC:LOF]]", 0),
    ("prelim", "List of Tables", "[[LOC:LOT]]", 0),
    ("chapter", "Chapter 1 Introduction and Problem Statement", "[[LOC:CH_1]]", 0),
    ("section", "1.1 Introduction", "[[LOC:SEC_1_1]]", 1),
    ("section", "1.2 Motivation", "[[LOC:SEC_1_2]]", 1),
    ("section", "1.3 Problem Statement", "[[LOC:SEC_1_3]]", 1),
    ("section", "1.4 Objectives and Project Scope", "[[LOC:SEC_1_4]]", 1),
    ("section", "1.5 Proposed Framework and Value Proposition", "[[LOC:SEC_1_5]]", 1),
    ("section", "1.6 Organization of the Project Report", "[[LOC:SEC_1_6]]", 1),
    ("chapter", "Chapter 2 Literature Review", "[[LOC:CH_2]]", 0),
    ("section", "2.1 Introduction", "[[LOC:SEC_2_1]]", 1),
    ("section", "2.2 Survey and Critical Evaluation of Existing Systems", "[[LOC:SEC_2_2]]", 1),
    ("section", "2.3 Theoretical Analysis of Recommendation Algorithms", "[[LOC:SEC_2_3]]", 1),
    ("section", "2.4 Architectural Paradigms: Monolithic vs. Distributed Microservices", "[[LOC:SEC_2_4]]", 1),
    ("section", "2.5 Modern Frontend Architectures: Vanilla JS vs. Heavy SPAs", "[[LOC:SEC_2_5]]", 1),
    ("section", "2.6 Identified Research and Practical Gaps", "[[LOC:SEC_2_6]]", 1),
    ("chapter", "Chapter 3 System Requirements and Architecture", "[[LOC:CH_3]]", 0),
    ("section", "3.1 Software Requirements Specification (SRS)", "[[LOC:SEC_3_1]]", 1),
    ("section", "3.2 Functional Requirements Matrix", "[[LOC:SEC_3_2]]", 1),
    ("section", "3.3 Non-Functional Requirements (NFR)", "[[LOC:SEC_3_3]]", 1),
    ("section", "3.4 Conceptual System Architecture and High-Level DFD", "[[LOC:SEC_3_4]]", 1),
    ("section", "3.5 UML Sequence Diagram for Booking Workflow", "[[LOC:SEC_3_5]]", 1),
    ("section", "3.6 Hardware and Software Operational Specifications", "[[LOC:SEC_3_6]]", 1),
    ("section", "3.7 Security and Compliance Requirements", "[[LOC:SEC_3_7]]", 1),
    ("chapter", "Chapter 4 Database Design and Relational Modeling", "[[LOC:CH_4]]", 0),
    ("section", "4.1 Relational Architecture and Normalization Strategy", "[[LOC:SEC_4_1]]", 1),
    ("section", "4.2 Entity-Relationship (ER) Modeling", "[[LOC:SEC_4_2]]", 1),
    ("section", "4.3 Comprehensive Relational Data Dictionary", "[[LOC:SEC_4_3]]", 1),
    ("section", "4.4 Database Normalization Analysis", "[[LOC:SEC_4_4]]", 1),
    ("section", "4.5 Indexing Strategy and Referential Integrity", "[[LOC:SEC_4_5]]", 1),
    ("chapter", "Chapter 5 Backend and Machine Learning Microservice Implementation", "[[LOC:CH_5]]", 0),
    ("section", "5.1 Spring Boot Core Backend Architecture", "[[LOC:SEC_5_1]]", 1),
    ("section", "5.2 Standardized API Envelope Pattern", "[[LOC:SEC_5_2]]", 1),
    ("section", "5.3 Security Architecture: Spring Security and Stateless JWT", "[[LOC:SEC_5_3]]", 1),
    ("section", "5.4 Machine Learning Recommendation Microservice", "[[LOC:SEC_5_4]]", 1),
    ("section", "5.5 Fault-Tolerant Fallback Integration in Spring Boot", "[[LOC:SEC_5_5]]", 1),
    ("chapter", "Chapter 6 Frontend UI/UX Design System", "[[LOC:CH_6]]", 0),
    ("section", "6.1 Introduction", "[[LOC:SEC_6_1]]", 1),
    ("section", "6.2 Design Philosophy and Visual Design System", "[[LOC:SEC_6_2]]", 1),
    ("section", "6.3 Modular Client-Side JavaScript Architecture", "[[LOC:SEC_6_3]]", 1),
    ("section", "6.4 Public Portals and User Flows", "[[LOC:SEC_6_4]]", 1),
    ("section", "6.5 Self-Service User and Admin Management Portals", "[[LOC:SEC_6_5]]", 1),
    ("chapter", "Chapter 7 Verification, Testing, and System Walkthrough", "[[LOC:CH_7]]", 0),
    ("section", "7.1 Introduction", "[[LOC:SEC_7_1]]", 1),
    ("section", "7.2 Testing Methodologies and Verification Strategy", "[[LOC:SEC_7_2]]", 1),
    ("section", "7.3 Comprehensive Test Cases and Execution Results", "[[LOC:SEC_7_3]]", 1),
    ("section", "7.4 Security Vulnerability and Penetration Testing", "[[LOC:SEC_7_4]]", 1),
    ("section", "7.5 Machine Learning Engine and Resilience Fallback Evaluation", "[[LOC:SEC_7_5]]", 1),
    ("section", "7.6 Automated Mobile Viewport and Smoke Testing", "[[LOC:SEC_7_6]]", 1),
    ("section", "7.7 Comprehensive Visual Walkthrough of Running System", "[[LOC:SEC_7_7]]", 1),
    ("chapter", "Chapter 8 Deployment, Cloud Hosting, and Local Operations", "[[LOC:CH_8]]", 0),
    ("section", "8.1 Introduction", "[[LOC:SEC_8_1]]", 1),
    ("section", "8.2 Free-Tier Production Cloud Hosting Topology", "[[LOC:SEC_8_2]]", 1),
    ("section", "8.3 Multi-Service Containerization and Docker Configurations", "[[LOC:SEC_8_3]]", 1),
    ("section", "8.4 Edge Routing and Reverse Proxy Rewrites", "[[LOC:SEC_8_4]]", 1),
    ("section", "8.5 Static Edge Hosting with Vercel", "[[LOC:SEC_8_5]]", 1),
    ("section", "8.6 Local Startup and Development Runbook", "[[LOC:SEC_8_6]]", 1),
    ("section", "8.7 Continuous Integration with GitHub Actions", "[[LOC:SEC_8_7]]", 1),
    ("chapter", "Chapter 9 Conclusion and Future Scope", "[[LOC:CH_9]]", 0),
    ("section", "9.1 Summary of Contributions and Completed Milestones", "[[LOC:SEC_9_1]]", 1),
    ("section", "9.2 Societal and Economic Impact in Uttarakhand", "[[LOC:SEC_9_2]]", 1),
    ("section", "9.3 Lessons Learned During System Development", "[[LOC:SEC_9_3]]", 1),
    ("section", "9.4 Limitations of the Current Implementation", "[[LOC:SEC_9_4]]", 1),
    ("section", "9.5 Suggestions for Future Work and Technical Roadmap", "[[LOC:SEC_9_5]]", 1),
    ("section", "9.6 Concluding Remarks", "[[LOC:SEC_9_6]]", 1),
    ("chapter", "References", "[[LOC:REFERENCES]]", 0),
]

FIGURE_DEFINITIONS = [
    ("1.1", "High-Level Distributed Framework of the StayMart Platform", "[[LOC:FIG_1_1]]"),
    ("2.1", "Distributed Microservice Deployment Topology vs. Monolithic Boundaries", "[[LOC:FIG_2_1]]"),
    ("3.1", "Data Flow Diagram Level 0 (Context Level Diagram) for the StayMart System", "[[LOC:FIG_3_1]]"),
    ("3.2", "UML Sequence Diagram: Accommodation Booking and Confirmation Flow", "[[LOC:FIG_3_2]]"),
    ("4.1", "Entity-Relationship (ER) Diagram of the StayMart Relational Database Schema", "[[LOC:FIG_4_1]]"),
    ("5.1", "Springdoc OpenAPI 3.0 Swagger UI Exposing Core Backend REST Endpoints", "[[LOC:FIG_5_1]]"),
    ("5.2", "Machine Learning Content-Based Recommendation Pipeline with TF-IDF Vectorization", "[[LOC:FIG_5_2]]"),
    ("6.1", "StayMart Public Landing Page Featuring Commercial Header, Campus Chips, and Category Discovery", "[[LOC:FIG_6_1]]"),
    ("6.2", "Authentication Portals Featuring Clean Credential Inputs and Password Visibility Toggles", "[[LOC:FIG_6_2]]"),
    ("6.3", "Faceted Search Portals Featuring Authentic Verified Photography", "[[LOC:FIG_6_3]]"),
    ("6.4", "Listing Detail Pages Featuring Interactive Media Galleries and Direct Host Actions", "[[LOC:FIG_6_4]]"),
    ("6.5", "Self-Service Listing Creation Portals for Accommodations and Student Marketplace", "[[LOC:FIG_6_5]]"),
    ("6.6", "Self-Service User Dashboard and Real-Time Peer Messaging Interfaces", "[[LOC:FIG_6_6]]"),
    ("6.7", "Administrative Console Featuring Live Platform Metrics and Pre-Publication Moderation Queue", "[[LOC:FIG_6_7]]"),
    ("7.1", "Step 1: Accommodation Search with Faceted Filtering", "[[LOC:FIG_7_1]]"),
    ("7.2", "Step 2: Property Detail View with Room Selection Widget", "[[LOC:FIG_7_2]]"),
    ("7.3", "Step 3: Marketplace Product Discovery and Inspection", "[[LOC:FIG_7_3]]"),
    ("7.4", "Step 4: Peer-to-Peer Chat Between Student and Caretaker", "[[LOC:FIG_7_4]]"),
    ("7.5", "Step 5: Administrative Dashboard, Moderation Queue, and User Directory", "[[LOC:FIG_7_5]]"),
    ("7.6", "Step 6: User Booking Management and Reservation Status Lifecycle", "[[LOC:FIG_7_6]]"),
    ("8.1", "Production Multi-Service Cloud Hosting Topology Across Free-Tier Providers", "[[LOC:FIG_8_1]]"),
]

TABLE_DEFINITIONS = [
    ("2.1", "Comparative Feature Matrix: StayMart vs. Existing Commercial Platforms", "[[LOC:TAB_2_1]]"),
    ("3.1", "Comprehensive Functional Requirements Specification", "[[LOC:TAB_3_1]]"),
    ("3.2", "System Hardware and Software Operational Specifications", "[[LOC:TAB_3_2]]"),
    ("4.1", "Data Dictionary: users Table", "[[LOC:TAB_4_1]]"),
    ("4.2", "Data Dictionary: locations Table", "[[LOC:TAB_4_2]]"),
    ("4.3", "Data Dictionary: categories Table", "[[LOC:TAB_4_3]]"),
    ("4.4", "Data Dictionary: properties Table", "[[LOC:TAB_4_4]]"),
    ("4.5", "Data Dictionary: rooms Table", "[[LOC:TAB_4_5]]"),
    ("4.6", "Data Dictionary: products Table", "[[LOC:TAB_4_6]]"),
    ("7.1", "Software Test Execution Record", "[[LOC:TAB_7_1]]"),
]

def build_html_document(page_map=None):
    css = """
  @page {
    size: A4;
    margin-left: 3.5cm;
    margin-top: 2.5cm;
    margin-right: 1.25cm;
    margin-bottom: 2.0cm;
  }

  * { box-sizing: border-box; }

  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.60;
    color: #111;
    margin: 0;
    padding: 0;
    background: #fff;
  }

  p {
    text-align: justify;
    margin-bottom: 14px;
    text-indent: 0.35in;
  }

  .no-indent { text-indent: 0; }
  .page-break { page-break-before: always; }
  .avoid-break { page-break-inside: avoid; }

  h1.chapter-title {
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin-top: 18px;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
    line-height: 1.25;
  }

  h2.section-title {
    font-size: 13pt;
    font-weight: bold;
    margin-top: 14px;
    margin-bottom: 6px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 2px;
  }

  h3.subsection-title {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 4px;
  }

  h4.subsubsection-title {
    font-size: 11.5pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 8px;
    margin-bottom: 4px;
  }

  ol, ul {
    margin-top: 4px;
    margin-bottom: 8px;
    padding-left: 32px;
  }

  li {
    margin-bottom: 3px;
    text-align: justify;
  }

  ol.references-list {
    font-size: 10pt;
    line-height: 1.32;
    margin-top: 6px;
    margin-bottom: 0;
    padding-left: 28px;
  }

  ol.references-list li {
    margin-bottom: 4px;
    text-align: justify;
  }

  .table-container {
    margin: 12px 0;
    page-break-inside: avoid;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0 10px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }

  th, td {
    border: 1px solid #333;
    padding: 4px 6px;
    text-align: left;
    vertical-align: top;
  }

  th {
    background-color: #f2f2f2;
    font-weight: bold;
  }

  .table-caption, .figure-caption {
    font-size: 10pt;
    font-style: italic;
    margin-bottom: 4px;
    text-align: center;
  }

  .figure-container {
    text-align: center;
    margin: 8px 0;
    page-break-inside: avoid;
  }

  .figure-container img {
    max-width: 80%;
    max-height: 195px;
    object-fit: contain;
    height: auto;
    border: 1px solid #ddd;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  }

  .fig-ch5 img {
    max-height: 130px;
  }

  .fig-ch5.figure-container {
    margin: 6px 0;
  }

  .fig-ch6 img {
    max-height: 145px;
  }

  .fig-ch6.figure-container {
    margin: 6px 0;
  }

  .fig-ch7 img {
    max-height: 195px;
  }

  .subfig-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 3px;
  }

  .subfig {
    text-align: center;
    flex: 1;
    max-width: 48%;
  }

  .subfig img {
    max-width: 100%;
    max-height: 105px;
    object-fit: contain;
    height: auto;
    border: 1px solid #ddd;
  }

  .subfig-cap {
    font-size: 8.5pt;
    font-style: italic;
    margin-top: 2px;
  }

  .lof-table {
    width: 100%;
    border-collapse: collapse;
    margin: 4px 0 8px 0;
    font-size: 8pt;
    page-break-inside: avoid;
  }

  .lof-table th, .lof-table td {
    border: 1px solid #333;
    padding: 2.2px 5px;
    text-align: left;
    vertical-align: top;
    line-height: 1.15;
  }

  .lof-table th {
    background-color: #f2f2f2;
    font-weight: bold;
  }

  .code-container {
    background: #f8f8f8;
    border: 1px solid #ddd;
    border-left: 3px solid #002f34;
    font-family: 'Courier New', Courier, monospace;
    font-size: 8pt;
    line-height: 1.25;
    padding: 6px 8px;
    margin: 8px 0;
    overflow-x: auto;
    page-break-inside: avoid;
  }

  .code-container pre {
    margin: 0;
    white-space: pre-wrap;
    word-break: break-all;
  }

  .cover-sheet, .title-sheet {
    text-align: center;
    height: 240mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
    page-break-after: always;
  }

  .cover-title { font-size: 15pt; font-weight: bold; line-height: 1.25; }
  .cover-report { font-size: 12pt; font-weight: bold; margin-top: 8px; }
  .cover-sub { font-size: 11pt; font-style: italic; line-height: 1.25; margin-top: 6px; }
  .cover-of { font-size: 11pt; font-style: italic; margin-top: 3px; }
  .cover-degree { font-size: 11.5pt; font-weight: bold; margin-top: 5px; }
  .cover-by { font-size: 11pt; font-style: italic; margin-top: 6px; }
  .cover-team { margin-top: 4px; font-size: 11pt; font-weight: bold; line-height: 1.3; }
  .cover-super { font-size: 11pt; font-style: italic; margin-top: 6px; }
  .cover-mentor { font-size: 11.5pt; font-weight: bold; margin-top: 3px; }
  .cover-mentor-desig { font-size: 10pt; font-style: italic; margin-top: 1px; }
  .cover-logo { width: 1.75in; height: 1.75in; margin: 0 auto; display: block; }
  .cover-school { font-size: 13pt; font-weight: bold; line-height: 1.25; }
  .cover-date { font-size: 11.5pt; font-weight: bold; margin-top: 6px; }
  .decl-header { font-size: 14pt; font-weight: bold; text-align: center; text-decoration: underline; margin-bottom: 20px; margin-top: 20px; }
  .sig-block { margin-top: 30px; display: flex; justify-content: space-between; font-weight: bold; }

  .toc-row {
    display: flex;
    align-items: baseline;
    margin-bottom: 3px;
    font-size: 10pt;
  }
  .toc-title { padding-right: 4px; }
  .toc-leader { flex: 1; border-bottom: 1px dotted #555; margin: 0 4px; height: 0; transform: translateY(-4px); }
  .toc-page { padding-left: 4px; text-align: right; font-weight: bold; }

  .page-marker {
    font-size: 0.1pt;
    color: transparent;
    line-height: 0;
    display: inline-block;
    user-select: none;
    letter-spacing: normal !important;
    text-transform: none !important;
  }
"""

    toc_html = ""
    for item_type, title, marker, indent in TOC_DEFINITIONS:
        default_val = "i" if item_type == "prelim" else "1"
        disp_p = page_map.get(marker, default_val) if page_map else default_val
        bold_style = "font-weight: bold;" if item_type in ("chapter", "appendix") else ""
        top_margin = "margin-top: 6px;" if item_type in ("chapter", "appendix") else ""
        pad_left = f"padding-left: {indent * 16}px;" if indent > 0 else ""
        toc_html += f"""  <div class="toc-row" style="{bold_style} {top_margin} {pad_left}">
    <span class="toc-title">{title}</span>
    <span class="toc-leader"></span>
    <span class="toc-page">{disp_p}</span>
  </div>\n"""

    lof_rows = ""
    for fig_no, fig_title, marker in FIGURE_DEFINITIONS:
        disp_p = page_map.get(marker, "1") if page_map else "1"
        lof_rows += f"""    <tr>
      <td style="width: 12%;">{fig_no}</td>
      <td style="width: 76%;">{fig_title}</td>
      <td style="width: 12%; text-align: right; font-weight: bold;">{disp_p}</td>
    </tr>\n"""

    lot_rows = ""
    for tab_no, tab_title, marker in TABLE_DEFINITIONS:
        disp_p = page_map.get(marker, "1") if page_map else "1"
        lot_rows += f"""    <tr>
      <td style="width: 12%;">{tab_no}</td>
      <td style="width: 76%;">{tab_title}</td>
      <td style="width: 12%; text-align: right; font-weight: bold;">{disp_p}</td>
    </tr>\n"""

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>StayMart - Smart Student Housing and Campus Marketplace</title>
<style>{css}</style>
</head>
<body>

<!-- ANNEXURE II: COVER PAGE (EXACTLY PAGE 1) -->
<div class="cover-sheet">
  <div>
    <div class="cover-title">STAYMART: SMART STUDENT HOUSING AND CAMPUS MARKETPLACE</div>
    <div class="cover-report">A PROJECT REPORT</div>
    <div class="cover-sub">Submitted in partial fulfilment of the requirements<br>for the award of the degree</div>
    <div class="cover-of">of</div>
    <div class="cover-degree">BACHELOR OF COMPUTER APPLICATIONS</div>
    <div class="cover-by">by</div>
    <div class="cover-team">
      <div>DIVYANSH JOSHI</div>
      <div>GORAV KUMAR</div>
      <div>GORAV BHATT</div>
      <div>DIVYANSHU MEHRA</div>
    </div>
    <div class="cover-super">Under the supervision of</div>
    <div class="cover-mentor">Ms. TABISH RAO</div>
    <div class="cover-mentor-desig">Faculty Mentor, School of Computing</div>
  </div>

  <div>
    <img src="file:///D:/Mini5th/report/gehu_logo.png" class="cover-logo" alt="GEHU Seal">
  </div>

  <div>
    <div class="cover-school">
      SCHOOL OF COMPUTING,<br>
      GRAPHIC ERA HILL UNIVERSITY, CLEMENTOWN,<br>
      DEHRADUN-248002, UTTARAKHAND, INDIA
    </div>
    <div class="cover-date">NOVEMBER, 2026</div>
  </div>
</div>

<!-- ANNEXURE III: TITLE PAGE (EXACTLY PAGE 2) -->
<div class="title-sheet">
  <div>
    <div class="cover-title">STAYMART: SMART STUDENT HOUSING AND CAMPUS MARKETPLACE</div>
    <div class="cover-report" style="margin-top: 14px;">PROJECT REPORT</div>
    <div class="cover-by" style="margin-top: 8px;">by</div>
    <div class="cover-team" style="margin-top: 4px;">
      <div>DIVYANSH JOSHI</div>
      <div>GORAV KUMAR</div>
      <div>GORAV BHATT</div>
      <div>DIVYANSHU MEHRA</div>
    </div>
    <div class="cover-super" style="margin-top: 8px;">Under the supervision of</div>
    <div class="cover-mentor">Ms. TABISH RAO</div>
    <div class="cover-mentor-desig">Faculty Mentor, School of Computing</div>
  </div>

  <div>
    <img src="file:///D:/Mini5th/report/gehu_logo.png" class="cover-logo" alt="GEHU Seal">
  </div>

  <div>
    <div class="cover-school">
      School of Computing<br>
      GRAPHIC ERA HILL UNIVERSITY,<br>
      CLEMENTOWN, DEHRADUN-248002,<br>
      UTTARAKHAND, INDIA
    </div>
    <div class="cover-date" style="margin-top: 8px;">NOVEMBER, 2026</div>
  </div>
</div>

<!-- CANDIDATE'S DECLARATION (PAGE 3) -->
<div class="page-break">
  <span class="page-marker">[[LOC:DECLARATION]]</span>
  <div class="decl-header">CANDIDATE’S DECLARATION</div>
  <p>We hereby certify that the work which is being presented in the PROJECT REPORT entitled <strong>&ldquo;STAYMART: SMART STUDENT HOUSING AND CAMPUS MARKETPLACE&rdquo;</strong> in partial fulfillment of the requirements for the award of the Degree of <strong>Bachelor of Computer Applications</strong> and submitted in the School of Computing of the Graphic Era Hill University, Dehradun is an authentic record of our own work carried out under the supervision of <strong>Ms. Tabish Rao</strong>, Faculty Mentor, School of Computing, Graphic Era Hill University, Dehradun.</p>
  
  <p>The matter presented in this Project Report has not been submitted by us for the award of any other degree of this or any other institution.</p>

  <div style="margin-top: 25px;">
    <div style="font-weight: bold; font-size: 11pt; margin-bottom: 8px;">Signatures of the Candidates:</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 10.5pt;">
      <div><strong>DIVYANSH JOSHI</strong><br><span style="color: #555; font-size: 9.5pt;">School of Computing, GEHU</span></div>
      <div><strong>GORAV KUMAR</strong><br><span style="color: #555; font-size: 9.5pt;">School of Computing, GEHU</span></div>
      <div><strong>GORAV BHATT</strong><br><span style="color: #555; font-size: 9.5pt;">School of Computing, GEHU</span></div>
      <div><strong>DIVYANSHU MEHRA</strong><br><span style="color: #555; font-size: 9.5pt;">School of Computing, GEHU</span></div>
    </div>
  </div>

  <div style="margin-top: 25px;">
    <p class="no-indent" style="font-size: 11.5pt;">This is to certify that the above statement made by the candidates is correct to the best of my/our knowledge.</p>
  </div>

  <div class="sig-block" style="margin-top: 30px; font-size: 11pt;">
    <div>Date: November, 2026</div>
    <div style="text-align: right;">
      <div><strong>Signature of Mentor</strong></div>
      <div style="margin-top: 4px;"><strong>Ms. TABISH RAO</strong></div>
      <div style="font-size: 10pt; font-weight: normal; font-style: italic;">Faculty Mentor, School of Computing</div>
    </div>
  </div>
</div>

<!-- ABSTRACT (PAGE 4) -->
<div class="page-break">
  <span class="page-marker">[[LOC:ABSTRACT]]</span>
  <div style="font-size:14pt; font-weight:bold; text-align:center; margin-bottom:15px; margin-top:20px;">Abstract</div>
  <p>Finding safe, affordable rental accommodation near university campuses in Uttarakhand—particularly around educational clusters in Dehradun, Rishikesh, and Roorkee—is a persistent challenge for outstation students. Incoming students frequently face steep broker commissions, misleading photos, and unverified rental terms. Concurrently, graduating seniors struggle to sell functional room essentials such as study tables, desert coolers, reference books, and second-hand two-wheelers, while incoming juniors buy the exact same goods brand new at retail prices. General classifieds like OLX suffer from broker spam and lack room-level vacancy details, while platforms like Airbnb cater exclusively to short-term tourists on daily tariffs.</p>

  <p>To solve this practical problem, this project presents <strong>StayMart</strong>, an integrated student accommodation and campus re-commerce web application tailored for Uttarakhand. The platform is built on a decoupled multi-tier architecture: a Java 17 / Spring Boot 3.3 REST API handling core transactions and role-based access control with stateless JSON Web Tokens (JWT), a normalized MySQL 8.0 relational database with 12 tables, and an asynchronous Python 3.11 / Flask machine learning microservice running a TF-IDF and cosine similarity recommendation pipeline with automated database-driven fallbacks. The frontend is engineered using responsive vanilla HTML5, CSS3, and modern JavaScript inspired by familiar commercial classified interfaces (OLX and Amazon), avoiding heavy client-side framework overhead. Key features include zero-brokerage direct contact with verified property caretakers, peer-to-peer student messaging, room-level vacancy tracking, wishlist management, and an administrative moderation dashboard.</p>

  <p>System evaluation confirms sub-50ms database queries under typical loads, reliable recommendation fallbacks when the ML microservice is offline, and clean mobile responsiveness across standard viewports. This report details the software requirements, relational schema, algorithm design, system implementation, and zero-cost cloud deployment guidelines for the platform.</p>
</div>

<!-- ACKNOWLEDGEMENTS (PAGE 5) -->
<div class="page-break">
  <span class="page-marker">[[LOC:ACKNOWLEDGEMENTS]]</span>
  <div style="font-size:14pt; font-weight:bold; text-align:center; margin-bottom:15px; margin-top:20px;">Acknowledgements</div>
  <p>We express our sincere gratitude to our project supervisor and mentor, <strong>Ms. Tabish Rao</strong>, School of Computing, Graphic Era Hill University, Dehradun, for her continuous encouragement, expert technical guidance, and constructive feedback throughout the ideation, system design, and implementation of the StayMart platform. Her valuable suggestions during architecture and system reviews significantly shaped the robust implementation of both the Spring Boot core service and the Python machine learning recommendation engine.</p>

  <p>We also extend our heartfelt thanks to the Head of the Department and all esteemed faculty members of the School of Computing for providing the computing infrastructure, laboratory facilities, and academic encouragement essential for the successful completion of this major project.</p>

  <p>Finally, we are deeply grateful to our parents, families, and peers for their constant support, understanding, and assistance in user acceptance testing and interface evaluation across varied mobile and desktop environments.</p>

  <div style="margin-top: 30px;">
    <div style="font-weight: bold; font-size: 11pt; margin-bottom: 8px; text-align: right;">Signatures of Candidates:</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; text-align: right; font-size: 10pt;">
      <div><strong>DIVYANSH JOSHI</strong></div>
      <div><strong>GORAV KUMAR</strong></div>
      <div><strong>GORAV BHATT</strong></div>
      <div><strong>DIVYANSHU MEHRA</strong></div>
    </div>
    <div style="text-align: right; margin-top: 6px; font-size: 10pt; font-style: italic;">Bachelor of Computer Applications (BCA)<br>School of Computing, GEHU Dehradun</div>
  </div>
</div>

<!-- CONTENTS (PAGES 6-7) -->
<div class="page-break">
  <span class="page-marker">[[LOC:TOC]]</span>
  <div style="font-size:14pt; font-weight:bold; text-align:center; margin-bottom:15px; margin-top:20px;">Contents</div>
  {toc_html}
</div>

<!-- LIST OF ABBREVIATIONS (PAGE 8) -->
<div class="page-break">
  <span class="page-marker">[[LOC:LOA]]</span>
  <div style="font-size:14pt; font-weight:bold; text-align:center; margin-bottom:15px; margin-top:20px;">List of Abbreviations</div>
  <table style="font-size: 9pt;">
    <thead><tr><th style="width: 25%;">Abbreviation</th><th>Full Expansion</th><th style="width: 25%;">Abbreviation</th><th>Full Expansion</th></tr></thead>
    <tbody>
      <tr><td><strong>ACID</strong></td><td>Atomicity, Consistency, Isolation, Durability</td><td><strong>JWT</strong></td><td>JSON Web Token</td></tr>
      <tr><td><strong>API</strong></td><td>Application Programming Interface</td><td><strong>ML</strong></td><td>Machine Learning</td></tr>
      <tr><td><strong>BCNF</strong></td><td>Boyce-Codd Normal Form</td><td><strong>NLP</strong></td><td>Natural Language Processing</td></tr>
      <tr><td><strong>CORS</strong></td><td>Cross-Origin Resource Sharing</td><td><strong>ORM</strong></td><td>Object-Relational Mapping</td></tr>
      <tr><td><strong>CSS</strong></td><td>Cascading Style Sheets</td><td><strong>PG</strong></td><td>Paying Guest Accommodation</td></tr>
      <tr><td><strong>DFD</strong></td><td>Data Flow Diagram</td><td><strong>RBAC</strong></td><td>Role-Based Access Control</td></tr>
      <tr><td><strong>DTO</strong></td><td>Data Transfer Object</td><td><strong>REST</strong></td><td>Representational State Transfer</td></tr>
      <tr><td><strong>ERD</strong></td><td>Entity-Relationship Diagram</td><td><strong>SRS</strong></td><td>Software Requirements Specification</td></tr>
      <tr><td><strong>HTML</strong></td><td>HyperText Markup Language</td><td><strong>TF</strong></td><td>Term Frequency</td></tr>
      <tr><td><strong>HTTP</strong></td><td>Hypertext Transfer Protocol</td><td><strong>UI / UX</strong></td><td>User Interface / User Experience</td></tr>
      <tr><td><strong>IDF</strong></td><td>Inverse Document Frequency</td><td><strong>UML</strong></td><td>Unified Modeling Language</td></tr>
      <tr><td><strong>JPA</strong></td><td>Java Persistence API</td><td><strong>WSGI</strong></td><td>Web Server Gateway Interface</td></tr>
      <tr><td><strong>JSON</strong></td><td>JavaScript Object Notation</td><td><strong>SPA</strong></td><td>Single Page Application</td></tr>
    </tbody>
  </table>
</div>

<!-- LIST OF FIGURES (PAGE 9) -->
<div class="page-break">
  <span class="page-marker">[[LOC:LOF]]</span>
  <div style="font-size:14pt; font-weight:bold; text-align:center; margin-bottom:12px; margin-top:16px;">List of Figures</div>
  <table class="lof-table">
    <thead><tr><th>Fig. No.</th><th>Title of Figure</th><th style="text-align: right;">Page</th></tr></thead>
    <tbody>
{lof_rows}
    </tbody>
  </table>
</div>

<!-- LIST OF TABLES (PAGE 10) -->
<div class="page-break">
  <span class="page-marker">[[LOC:LOT]]</span>
  <div style="font-size:14pt; font-weight:bold; text-align:center; margin-bottom:15px; margin-top:20px;">List of Tables</div>
  <table>
    <thead><tr><th>Table No.</th><th>Title of Table</th><th style="text-align: right;">Page</th></tr></thead>
    <tbody>
{lot_rows}
    </tbody>
  </table>
</div>
"""

    for ch in range(1, 10):
        if ch in chapters:
            doc += f'\n<div class="page-break">\n'
            doc += latex_to_html_content(chapters[ch], ch_num=ch)
            doc += '\n</div>\n'

    doc += """
<div class="page-break">
  <span class="page-marker">[[LOC:REFERENCES]]</span>
  <h1 class="chapter-title">References</h1>
  <ol class="references-list">
    <li>Adomavicius, G. and Tuzhilin, A., 2005. Toward the next generation of recommender systems: A survey of the state-of-the-art and possible extensions. <em>IEEE Transactions on Knowledge and Data Engineering</em>, 17(6), pp.734-749.</li>
    <li>Bauer, C., King, G. and Gregory, G., 2015. <em>Java Persistence with Hibernate, Second Edition</em>. Manning Publications.</li>
    <li>Burke, R., 2002. Hybrid recommender systems: Survey and experiments. <em>User Modeling and User-Adapted Interaction</em>, 12(4), pp.331-370.</li>
    <li>Fielding, R.T., 2000. <em>Architectural styles and the design of network-based software architectures</em>. Doctoral dissertation, University of California, Irvine.</li>
    <li>Fowler, M., 2002. <em>Patterns of Enterprise Application Architecture</em>. Addison-Wesley Professional.</li>
    <li>Gamma, E., Helm, R., Johnson, R. and Vlissides, J., 1994. <em>Design Patterns: Elements of Reusable Object-Oriented Software</em>. Addison-Wesley.</li>
    <li>Grigorik, I., 2013. <em>High Performance Browser Networking</em>. O'Reilly Media, Inc.</li>
    <li>Kleppmann, M., 2017. <em>Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems</em>. O'Reilly Media, Inc.</li>
    <li>Koren, Y., Bell, R. and Volinsky, C., 2009. Matrix factorization techniques for recommender systems. <em>Computer</em>, 42(8), pp.30-37.</li>
    <li>Lops, P., De Gemmis, M. and Semeraro, G., 2011. Content-based recommender systems: State of the art and trends. In <em>Recommender Systems Handbook</em> (pp. 73-105). Springer.</li>
    <li>Newman, S., 2021. <em>Building Microservices: Designing Fine-Grained Systems, Second Edition</em>. O'Reilly Media, Inc.</li>
    <li>Pedregosa, F. et al., 2011. Scikit-learn: Machine Learning in Python. <em>Journal of Machine Learning Research</em>, 12, pp.2825-2830.</li>
    <li>Resnick, P. and Varian, H.R., 1997. Recommender systems. <em>Communications of the ACM</em>, 40(3), pp.56-58.</li>
    <li>Ricci, F., Rokach, L. and Shapira, B., 2015. <em>Recommender Systems Handbook</em>. Springer.</li>
    <li>Salton, G. and Buckley, C., 1988. Term-weighting approaches in automatic text retrieval. <em>Information Processing & Management</em>, 24(5), pp.513-523.</li>
    <li>Sarwar, B., Karypis, G., Konstan, J. and Riedl, J., 2001. Item-based collaborative filtering recommendation algorithms. In <em>Proceedings of the 10th International Conference on World Wide Web</em> (pp. 285-295).</li>
    <li>Schafer, J.B., Frankowski, D., Herlocker, J. and Sen, S., 2001. E-commerce recommendation applications. <em>Data Mining and Knowledge Discovery</em>, 5(1), pp.115-153.</li>
    <li>Silberschatz, A., Korth, H.F. and Sudarshan, S., 2020. <em>Database System Concepts, Seventh Edition</em>. McGraw-Hill Education.</li>
    <li>Turnbull, J., 2016. <em>The Docker Book: Containerization is the new virtualization</em>. James Turnbull.</li>
    <li>Walls, C., 2022. <em>Spring in Action, Sixth Edition</em>. Manning Publications.</li>
  </ol>
</div>
</body></html>"""
    return doc

def run_chrome_pdf(html_path, pdf_path):
    temp_user_dir = r"C:\Users\divya\AppData\Local\Temp\chrome_report_profile"
    cmd = [
        CHROME,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--user-data-dir={temp_user_dir}",
        f"--print-to-pdf={pdf_path}",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Chrome error: {res.stderr}")

def extract_marker_pages(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    marker_pages = {}
    pattern = re.compile(r'\[\s*\[\s*L\s*O\s*C\s*:\s*([A-Za-z0-9_ ]+?)\s*\]\s*\]')
    for p_num, page in enumerate(reader.pages, 1):
        txt = page.extract_text()
        for m in pattern.finditer(txt):
            key = f"[[LOC:{m.group(1).replace(' ', '')}]]"
            if key not in marker_pages:
                marker_pages[key] = p_num
    return marker_pages, len(reader.pages)

def compile_full_report():
    print("\n--- Pass 1: Discovering Item Locations ---")
    pass1_html = build_html_document(page_map=None)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(pass1_html)

    run_chrome_pdf(OUTPUT_HTML, TEMP_PASS1_PDF)
    marker_pages_p1, total_pages_p1 = extract_marker_pages(TEMP_PASS1_PDF)
    p_ch1_p1 = marker_pages_p1.get("[[LOC:CH_1]]", 11)
    print(f"Pass 1 complete: {total_pages_p1} pages generated. Chapter 1 begins on physical Page {p_ch1_p1}.")

    page_map = {}
    for m, p in marker_pages_p1.items():
        if p < p_ch1_p1:
            page_map[m] = to_roman(p - 2) if p > 2 else ""
        else:
            page_map[m] = str(p - p_ch1_p1 + 1)

    print("\n--- Pass 2: Rendering TOC & Lists with True Page Numbers ---")
    pass2_html = build_html_document(page_map=page_map)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(pass2_html)

    run_chrome_pdf(OUTPUT_HTML, TEMP_PASS2_PDF)
    marker_pages_p2, total_pages_p2 = extract_marker_pages(TEMP_PASS2_PDF)
    p_ch1_p2 = marker_pages_p2.get("[[LOC:CH_1]]", 11)
    print(f"Pass 2 complete: {total_pages_p2} pages generated. Chapter 1 begins on physical Page {p_ch1_p2}.")

    drift = abs(total_pages_p2 - total_pages_p1)
    if drift == 0:
        print("CONVERGENCE VERIFIED: 0 page drift between Pass 1 and Pass 2!")
    else:
        print(f"Warning: {drift} page drift detected.")

    print("\n--- Pass 3: Generating and Merging Two-Tier Page Numbers ---")
    overlay_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{ size: A4; margin: 0; }}
body {{ margin: 0; padding: 0; font-family: 'Times New Roman', Times, serif; }}
.sheet {{ width: 210mm; height: 297mm; position: relative; page-break-after: always; box-sizing: border-box; }}
.page-num {{ position: absolute; bottom: 1.0cm; left: 0; width: 100%; text-align: center; font-size: 11pt; color: #111; }}
</style>
</head>
<body>
"""
    for p in range(1, total_pages_p2 + 1):
        if p in (1, 2):
            disp_num = ""
        elif p < p_ch1_p2:
            disp_num = to_roman(p - 2)
        else:
            disp_num = str(p - p_ch1_p2 + 1)

        num_div = f'<div class="page-num">{disp_num}</div>' if disp_num else ''
        overlay_html += f'<div class="sheet">{num_div}</div>\n'

    overlay_html += "</body></html>"
    with open(OVERLAY_HTML, 'w', encoding='utf-8') as f:
        f.write(overlay_html)

    run_chrome_pdf(OVERLAY_HTML, OVERLAY_PDF)

    doc_reader = pypdf.PdfReader(TEMP_PASS2_PDF)
    overlay_reader = pypdf.PdfReader(OVERLAY_PDF)
    writer = pypdf.PdfWriter()

    for idx, page in enumerate(doc_reader.pages):
        if idx < len(overlay_reader.pages):
            page.merge_page(overlay_reader.pages[idx])
        writer.add_page(page)

    with open(OUTPUT_PDF, 'wb') as f:
        writer.write(f)

    final_size = os.path.getsize(OUTPUT_PDF)
    print(f"\nSUCCESS: Compiled final report to {OUTPUT_PDF}")
    print(f"Total Pages: {len(writer.pages)}, File Size: {final_size} bytes ({final_size / (1024*1024):.2f} MB)")

    for temp_f in [TEMP_PASS1_PDF, TEMP_PASS2_PDF, OVERLAY_HTML, OVERLAY_PDF]:
        if os.path.exists(temp_f):
            try:
                os.remove(temp_f)
            except Exception:
                pass

if __name__ == '__main__':
    compile_full_report()
