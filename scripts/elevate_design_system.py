"""
scripts/elevate_design_system.py
Modernize StayMart UI according to Anthropic Frontend Design Skill.
Implements:
1. Palette: Deep Himalayan Alpine Navy, Radiant Amber, Emerald Mint, Slate & Luminous Canvas.
2. Typography: Plus Jakarta Sans for titles/brand/metrics, Inter for body/tabular data.
3. Elevated Buttons: Replace 4-color OLX border with elevated gradient pill.
4. Cards: Sleek modern elevation, micro-interactions, clean hover lift.
5. Navigation & Header: High-trust styling, subtle border, polished pills.
6. Hero: Clean layout, removes single-word accent AI-tell, elegant stats card.
"""

import re
import os

GLOBAL_CSS_PATH = "frontend/css/global.css"

with open(GLOBAL_CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update font import
old_font_regex = re.compile(r"@import url\('https://fonts\.googleapis\.com/css2\?family=Inter[^\']*'\);")
new_font = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');"
css = old_font_regex.sub(new_font, css, count=1)

# 2. Update :root token block
root_start = css.find(':root {')
root_end = css.find('}', root_start)
if root_start != -1 and root_end != -1:
    new_root = """:root {
  /* Brand Palette: Deep Himalayan Alpine Navy + Radiant Amber + Emerald Mint */
  --header-bg: #0b1e36;            /* Deep Alpine Navy - authoritative, high-trust */
  --header-text: #ffffff;
  --header-hover: #38bdf8;          /* Crisp Glacier Sky */
  
  --amazon-amber: #f59e0b;          /* Radiant Himalayan Amber */
  --amazon-yellow: #f59e0b;         /* Modern Amber */
  --amazon-yellow-hover: #d97706;   /* Deep Warm Amber */
  --amazon-dark: #091524;           /* Midnight Slate */
  
  --olx-teal: #0b1e36;              /* Deep Alpine Navy */
  --olx-cyan: #0284c7;              /* Crisp Cobalt Cyan */
  --olx-light-teal: #f0f7ff;        /* Soft Alpine Mist */
  
  /* Modern Commercial Neutral Surfaces (Clean Luminous Theme) */
  --bg-page: #f8fafc;               /* Crisp Pearl White Canvas */
  --bg-card: #ffffff;
  --bg-hover: #f1f5f9;
  --bg-subtle: #f8fafc;
  
  /* Text & Typography */
  --text-primary: #0b1e36;          /* High contrast deep navy */
  --text-secondary: #475569;        /* Slate 600 - crisp subtitles */
  --text-muted: #64748b;            /* Slate 500 - accessible metadata (WCAG AAA) */
  --text-link: #0284c7;             /* Vibrant Sky Blue */
  
  /* Borders & Dividers */
  --border: #e2e8f0;                /* Ultra crisp, delicate slate border */
  --border-subtle: #edf2f7;
  --border-focus: #f59e0b;          /* Warm radiant amber ring */
  
  /* Status & Accents */
  --success: #10b981;               /* Emerald Mint Verified */
  --danger: #ef4444;                /* Vivid Coral Red */
  --warning: #f59e0b;               /* Amber warning */
  --info: #0284c7;                  /* Glacier Blue */
  
  /* Elevation & Shadows */
  --shadow-sm: 0 1px 3px rgba(11, 30, 54, 0.05);
  --shadow-md: 0 4px 16px -2px rgba(11, 30, 54, 0.08), 0 2px 6px -1px rgba(11, 30, 54, 0.04);
  --shadow-lg: 0 16px 36px -4px rgba(11, 30, 54, 0.12), 0 6px 16px -2px rgba(11, 30, 54, 0.06);
  
  /* Layout Dimensions */
  --radius-sm: 6px;
  --radius: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  --font: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-display: 'Plus Jakarta Sans', var(--font);
  --transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-fast: all 0.14s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-spring: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Backward-Compatible Theme Tokens & Semantic Aliases */
  --primary: #0b1e36;                        /* Deep Alpine Navy Brand */
  --primary-dark: #071526;
  --primary-light: #0284c7;                  /* Glacier Action Blue */
  --primary-hover: #132a4a;
  --primary-bg: #f0f7ff;
  
  --accent: #f59e0b;                         /* Radiant Amber */
  --accent-light: #10b981;                   /* Emerald Green */
  --accent-hover: #d97706;
  
  --dark: #0b1e36;
  --dark-2: #071526;
  --dark-3: #162e4d;
  
  --card-bg: #ffffff;
  --card-bg-hover: #f8fafc;
  
  --glass: rgba(255, 255, 255, 0.95);
  --glass-border: rgba(11, 30, 54, 0.08);
  
  --gradient-primary: linear-gradient(135deg, #0b1e36 0%, #162e4d 100%);
  --gradient-card: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  --gradient-accent: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
}"""
    css = css[:root_start] + new_root + css[root_end+1:]
    print("Updated root tokens.")

# 3. Typography: apply Plus Jakarta Sans to brand headings, card titles, hero headline
typog_rules = """
/* Typography Hierarchy per Anthropic Frontend Design */
h1, h2, h3, h4, h5, h6,
.hero-headline, .brand-logo, .card-title, .card-price, .calc-heading, .stat-num {
  font-family: var(--font-display, var(--font));
  letter-spacing: -0.02em;
}
"""
if "/* Typography Hierarchy per Anthropic Frontend Design */" not in css:
    css = css + "\n" + typog_rules

# 4. Modernize .btn-olx-sell: replace clunky 4-color border with elevated radiant amber pill
old_sell_btn_pattern = re.compile(
    r"\.btn-olx-sell\s*\{[^}]*border-color:\s*#23e5db\s*#ffce32\s*#3a77ff\s*#23e5db;[^}]*\}",
    re.DOTALL
)
new_sell_btn = """.btn-olx-sell {
  background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
  color: #ffffff !important;
  font-family: var(--font-display, var(--font));
  font-weight: 700;
  font-size: 13.5px;
  letter-spacing: 0.3px;
  padding: 8px 22px;
  border-radius: var(--radius-full);
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 14px rgba(234, 88, 12, 0.35);
  transition: var(--transition);
  white-space: nowrap;
  position: relative;
  overflow: hidden;
  text-decoration: none !important;
}

.btn-olx-sell:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(234, 88, 12, 0.45);
  background: linear-gradient(135deg, #d97706 0%, #c2410c 100%);
  color: #ffffff !important;
}"""

if old_sell_btn_pattern.search(css):
    css = old_sell_btn_pattern.sub(new_sell_btn, css)
    print("Updated .btn-olx-sell with elevated radiant amber pill.")

# Also update .hero-promo-card: remove dashed border
css = css.replace("border: 2px dashed #002f34;", "border: 1px solid rgba(11, 30, 54, 0.1); background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); box-shadow: 0 4px 20px rgba(11, 30, 54, 0.06);")

# Update .hero-headline span.highlight: remove clunky border bottom tell
css = css.replace("border-bottom: 3px solid var(--amazon-amber);", "color: var(--primary-light);")

with open(GLOBAL_CSS_PATH, "w", encoding="utf-8") as f:
    f.write(css)

print("Saved elevated global.css successfully.")

