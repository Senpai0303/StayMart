## 2026-11-03T06:38:03Z
You are m2_worker, a teamwork_worker.
Working directory: d:\Mini5th\.agents\teamwork\m2_worker

You MUST read:
- d:\Mini5th\.agents\teamwork\ORIGINAL_REQUEST.md
- d:\Mini5th\.agents\teamwork\orchestrator\SCOPE.md
- d:\Mini5th\.agents\teamwork\survey_spec_miner_report\handoff.md
- d:\Mini5th\project report format.pdf
- d:\Mini5th\report\main.tex
- d:\Mini5th\scripts\compile_report_pdf.py

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your write ownership:
- You own: `report/main.tex`, `report/chapters/*.tex` (if needed for references/formatting), `scripts/compile_report_pdf.py`, and compiling the final document `d:\Mini5th\StayMart_Project_Report.pdf`.

Objective:
Execute Milestone 2 / Requirement R1 (LaTeX Project Report Formatting & Compilation):
1. Harmonize `report/main.tex`:
   - Update Candidate Declaration text to the exact verbatim Graphic Era Hill University wording specified in `project report format.pdf` (Pages 7-8).
   - Add proper TOC entries (`\addcontentsline{toc}{chapter}{Abstract}`, `\addcontentsline{toc}{chapter}{Acknowledgements}`).
   - Update bibliography style to `\bibliographystyle{plain}` so references are alphabetized by author name per Rule 5.
2. Upgrade `scripts/compile_report_pdf.py`:
   - Calibrate Cover Page (Annexure II) CSS so all elements (Title, Degree, Candidate, Supervisor, Seal 1.75"x1.75", School of Computing, Date) fit cleanly on exactly Page 1 without overflowing to Page 2.
   - Calibrate Title Page (Annexure III) CSS so all elements fit cleanly on exactly Page 2.
   - Suppress browser print headers/footers (add `--no-pdf-header-footer` to Chrome execution arguments) to completely eliminate timestamps and `file:///...` URLs.
   - Implement clean two-tier page numbering: unnumbered Cover (p. 1) & Title (p. 2); lowercase Roman numerals (`i`, `ii`, `iii`, ...) centered at bottom for Preliminary Pages (Declaration, Abstract, Acknowledgements, TOC, List of Abbreviations, List of Figures, List of Tables); restart Arabic page numbering at `1` on Chapter 1 Introduction.
   - Implement dynamic two-pass pagination so that the Table of Contents, List of Figures, and List of Tables display the true, exact page numbers where each chapter, section, figure, and table appears in the generated PDF (zero page number drift).
3. Execute the compilation script:
   - Compile `d:\Mini5th\StayMart_Project_Report.pdf`.
   - Verify the PDF using Python / `pypdf`: assert file exists, size > 1MB, total page count, clean 1-page Cover, clean 1-page Title, Roman numerals on preliminary pages, Arabic numerals on body pages, and verify TOC page numbers match actual chapter locations.

Write your full handoff report to `d:\Mini5th\.agents\teamwork\m2_worker\handoff.md`.
Use `send_message` to notify the orchestrator (conversation ID: d3594b73-38bb-4954-9403-d6c5dcb5954a) once complete.
