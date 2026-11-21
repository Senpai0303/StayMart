# Project: StayMart Academic Project Report & Frontend Modernization

## Architecture
StayMart is a university student accommodation and re-commerce marketplace in Uttarakhand.
- **Documentation & Report**: Academic project report in `report/` (`report/main.tex` and `report/chapters/*.tex`) compiled to `StayMart_Project_Report.pdf` conforming strictly to Graphic Era Hill University specifications (`project report format.pdf`).
- **Design System & Skill**: Anthropic `frontend-design` skill installed under `.agents/skills/frontend-design/` via official npm CLI package `skills@latest`.
- **Frontend**: Multi-Page Application (27 HTML files, 2 CSS stylesheets, 29 JS controllers) in `frontend/` styled with modern, premium "Himalayan Modern" design tokens, elevated typography, purposeful micro-interactions, responsive across 320px–1920px viewports without horizontal overflow or broken links.
- **Backend & ML**: Spring Boot 3.3.5 (Java 17) REST API and Flask ML recommendation service.
- **Verification Harness**: Automated multi-suite testing pipeline in `scripts/` (`run_viewport_tests.js`, `run_all_verifications.py`, `compile_report_pdf.py`, `run_smoke_tests.py`, `verify_m1_navigation.py`, `scan_ai_artifacts.py`).

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Skill CLI Installation | Install Anthropic `frontend-design` skill via `npx -y skills@latest add anthropics/skills --skill frontend-design --agent antigravity -y` | M1 | Survey S3 |
| 2 | Skill Filesystem Verification | Verify `.agents/skills/frontend-design/SKILL.md`, `LICENSE.txt`, and tracking in `skills-lock.json` and `npx -y skills@latest list --json` | M1 | Survey S3 |
| 3 | LaTeX Institutional Margin & Geometry | Enforce Left 3.5cm, Top 2.5cm, Right 1.25cm, Bottom 1.25cm margins on A4 executive paper in `report/main.tex` and compiler | M2 | Survey S1 |
| 4 | Cover & Title Page Layouts | Single-page Annexure II Cover and Annexure III Title pages with exact GEHU formatting, seal size 1.75"x1.75", bold uppercase titles | M2 | Survey S1 |
| 5 | Candidate Declaration & Certification | Formatted Candidate's Declaration and Mentor Certificate with exact verbatim institutional wording and bold inverted title | M2 | Survey S1 |
| 6 | Abstract & Acknowledgements | Standalone Abstract (strictly < 300 words, actual 273 words) and Acknowledgements with Roman numerals and TOC entries | M2 | Survey S1 |
| 7 | Two-Tier Dynamic Pagination | Unnumbered Cover/Title, lowercase Roman numerals (`i`..`vii`) on preliminary pages, restart Arabic `1` on Chapter 1 | M2 | Survey S1 |
| 8 | Two-Pass Dynamic Table of Contents | Dynamic calculation of exact page numbers for TOC, List of Figures, List of Tables with dotted leader lines (0 page drift) | M2 | Survey S1 |
| 9 | Browser Chrome Header Suppression | Pass `--no-pdf-header-footer` to Chrome Headless print engine to eliminate URL and timestamp stamps | M2 | Survey S1 |
| 10 | Alphabetical References | Format `report/references.bib` with `plain` bibliographic style in alphabetical order by author name | M2 | Survey S1 |
| 11 | Final PDF Compilation | Compile complete, flawless academic PDF at `d:\Mini5th\StayMart_Project_Report.pdf` (> 5MB, cleanly formatted) | M2 | Survey S1 |
| 12 | Himalayan Modern Token System | Unified 4-6 named hex tokens in `global.css` & `dashboard.css` (Deep Pine `#0f2e28`, Warm Ochre `#d97724`, Alpine Sage `#2d7a5b`, Alabaster `#f8faf8`) | M3 | Survey S2 |
| 13 | Typographic Elevation | Plus Jakarta Sans display headlines paired with Inter body text, proportional typographic scale, 0 raw emoji clutter in headings | M3 | Survey S2 |
| 14 | Card De-Cluttering & Visual Polish | Streamline property & product cards to 3 clear visual tiers (photography, price, campus/category tag, title, locality) | M3 | Survey S2 |
| 15 | Header & Navigation Overhaul | Streamlined Himalayan Pine navbar, segmented campus search pill, refined action buttons (remove 4-color OLX border) | M3 | Survey S2 |
| 16 | Public Hub & Detail Modernization | Elevate hero banner, metric ribbons, campus pills, dual-mode savings calculator, photo gallery lightbox, and sticky mobile action bars | M3 | Survey S2 |
| 17 | User & Admin Space Polish | Cohesive sidebar navigation, enterprise tables with status badges, split-panel chat interface, and cohesive analytics charts | M3 | Survey S2 |
| 18 | Multi-Viewport Layout Integrity | 0 horizontal overflow across 320px, 375px, 414px, 768px, 1280px, 1920px viewports (`docScrollWidth <= vpWidth`) | M4 | Survey S3 |
| 19 | Mobile Component & Sheet Interactivity | Responsive visibility of `#mobileMenuToggle`, `#mobileSearchTrigger`, and clean opening of mobile filter and booking drawers | M4 | Survey S3 |
| 20 | Static Asset & Navigation Integrity | 0 missing scripts, 0 missing stylesheets, 0 broken links across all 27 HTML pages and 29 JS controllers | M4 | Survey S3 |
| 21 | Unified Master Pipeline Certification | Execute `python scripts/run_all_verifications.py` asserting 7/7 suites pass with exit code 0 | M4 | Survey S3 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Anthropic Frontend Design Skill Installation & Verification | Features 1–2: Run CLI installation command and verify files under `.agents/skills/` | None | DONE |
| M2 | LaTeX Project Report Formatting & Compilation (`StayMart_Project_Report.pdf`) | Features 3–11: Fix `report/main.tex`, update `scripts/compile_report_pdf.py`, generate flawless PDF | None | IN_PROGRESS |
| M3 | Modern Premium Frontend Redesign (All Pages & Viewports) | Features 12–17: Apply Himalayan Modern design tokens, typography, card decluttering, header overhaul across all 27 HTML pages | M1 | PLANNED |
| M4 | Comprehensive Multi-Viewport Verification & Master Pipeline Certification | Features 18–21: Run `run_viewport_tests.js`, `verify_m1_navigation.py`, `run_all_verifications.py` | M1, M2, M3 | PLANNED |

---

## Interface Contracts

### Skill CLI ↔ Repository Architecture
- Command: `npx -y skills@latest add anthropics/skills --skill frontend-design --agent antigravity -y`
- Filesystem: `.agents/skills/frontend-design/SKILL.md` (size >= 9000 bytes), `LICENSE.txt`.
- Lockfile: `skills-lock.json` containing `frontend-design` entry.
- CLI Telemetry: `npx -y skills@latest list --json` returns status `tracked`.

### LaTeX Report ↔ Official Institutional Standard (`project report format.pdf`)
- Margins: Left 3.5cm, Top 2.5cm, Right 1.25cm, Bottom 1.25cm on A4.
- Typography: Times New Roman 12pt, 1.5 line spacing.
- Preliminary Pages: Cover (Annexure II), Title (Annexure III), Declaration (verbatim GEHU text), Abstract (< 300 words), Acknowledgements, TOC with dotted leaders, List of Abbreviations, List of Figures, List of Tables.
- Pagination: Cover/Title unnumbered, Preliminary pages Roman numerals (`i`..`vii`), Body pages Arabic starting at `1`.
- Clean compilation: No browser URLs or timestamps on pages (`--no-pdf-header-footer`).
- Target Output: `d:\Mini5th\StayMart_Project_Report.pdf`.

### Frontend Redesign ↔ Design System & API Integration
- CSS Base Tokens: `--color-brand-primary: #0f2e28;`, `--color-brand-accent: #d97724;`, `--color-brand-sage: #2d7a5b;`, `--color-surface-page: #f8faf8;`, `--color-surface-card: #ffffff;`.
- Responsive Viewports: 320px, 375px, 414px, 768px, 1280px, 1920px. `docScrollWidth <= clientWidth`.
- API Contract: Retain all 74 endpoint mappings in `frontend/js/api.js`. Zero regressions in auth, booking, orders, or search queries.
