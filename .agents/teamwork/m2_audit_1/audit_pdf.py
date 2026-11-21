import os
import pypdf

PDF_PATH = r"d:\Mini5th\StayMart_Project_Report.pdf"

reader = pypdf.PdfReader(PDF_PATH)
meta = reader.metadata
print("PDF Metadata:")
for k, v in meta.items():
    print(f"  {k}: {v}")
print(f"Total pages: {len(reader.pages)}")

# Extract all text once
all_texts = [p.extract_text() for p in reader.pages]

chapters_samples = [
    (1, "ch1_introduction.tex", "Every academic year, thousands of students from across India relocate to Uttarakhand"),
    (2, "ch2_literature_review.tex", "The evolution of online two-sided marketplaces and accommodation discovery networks"),
    (3, "ch3_requirements_architecture.tex", "The development of a resilient, distributed, two-sided marketplace requires rigorous requirements"),
    (4, "ch4_database_design.tex", "A marketplace platform handling real-time room bookings, peer-to-peer product orders"),
    (5, "ch5_backend_ml.tex", "StayMart's backend architecture is designed around a decoupled multi-tier setup"),
    (6, "ch6_frontend_ui.tex", "When designing StayMart's user interface, the primary architectural goal was to deliver an exceptionally modern"),
    (7, "ch7_testing_walkthrough.tex", "Testing a multi-tier student marketplace requires verifying backend business rules"),
    (8, "ch8_deployment_hosting.tex", "A major challenge when developing full-stack university software projects is hosting costs"),
    (9, "ch9_conclusion.tex", "In this project, we designed and built StayMart to address the everyday challenges students face")
]

print("\n--- Verifying Chapter Text Provenance in PDF ---")
for ch_num, ch_file, search_phrase in chapters_samples:
    found_pages = []
    for p_num, txt in enumerate(all_texts, 1):
        txt_norm = " ".join(txt.split())
        phrase_norm = " ".join(search_phrase.split())
        if phrase_norm.lower() in txt_norm.lower():
            found_pages.append(p_num)
    print(f"Chapter {ch_num} ({ch_file}): found on pages {found_pages}")
    assert len(found_pages) > 0, f"Missing phrase from {ch_file}: {search_phrase}"

# Verify Appendices
appendices_samples = [
    ("Appendix A", "app_backend_code.tex", "This appendix provides the authoritative source code listings for the core architectural components of the StayMart backend"),
    ("Appendix B", "app_frontend_code.tex", "This appendix provides the core client-side JavaScript architecture governing the StayMart frontend web portal"),
    ("Appendix C", "app_database_schema.tex", "This appendix documents the complete, authoritative Data Definition Language (DDL)"),
    ("Appendix D", "app_api_specs.tex", "This appendix provides the reference catalog of the 16 RESTful resource controllers")
]

print("\n--- Verifying Appendix Text Provenance in PDF ---")
for app_name, app_file, search_phrase in appendices_samples:
    found_pages = []
    for p_num, txt in enumerate(all_texts, 1):
        txt_norm = " ".join(txt.split())
        phrase_norm = " ".join(search_phrase.split())
        if phrase_norm.lower() in txt_norm.lower():
            found_pages.append(p_num)
    print(f"{app_name} ({app_file}): found on pages {found_pages}")
    assert len(found_pages) > 0, f"Missing phrase from {app_file}: {search_phrase}"

print("\nAll chapters and appendices successfully confirmed present in compiled PDF!")
