import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_OUTPUT = r"D:\Mini5th\StayMart_Work_Division_and_Architecture.docx"
MD_OUTPUT = r"D:\Mini5th\docs\WORK_DIVISION_AND_TECH_STACK.md"

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles setup
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(6)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.space_before = Pt(12)
    run_title = p_title.add_run("STAYMART: SMART STUDENT HOUSING AND CAMPUS MARKETPLACE")
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x00, 0x2F, 0x34) # Deep Teal

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(6)
    run_sub = p_sub.add_run("Team Work Allocation, Architectural Framework, Tech Stack & Implementation Guide")
    run_sub.font.name = 'Times New Roman'
    run_sub.font.size = Pt(13)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Academic metadata box
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(18)
    run_meta = p_meta.add_run("Degree: Bachelor of Computer Applications (BCA) | School of Computing\nGraphic Era Hill University (GEHU), Dehradun | Academic Year: 2026\nFaculty Mentor: Ms. Tabish Rao")
    run_meta.font.name = 'Times New Roman'
    run_meta.font.size = Pt(10.5)
    run_meta.font.bold = True
    run_meta.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    doc.add_heading("1. Executive Project Summary", level=1)
    p = doc.add_paragraph(
        "StayMart is a production-grade, distributed web platform specifically engineered to address the critical living and commerce "
        "challenges faced by tertiary students across university clusters in Uttarakhand (including Dehradun, Rishikesh, and Roorkee). "
        "The platform bridges two interconnected student requirements: (1) finding verified, affordable, zero-brokerage rental accommodation "
        "with real-time room vacancy tracking, and (2) an intra-campus re-commerce marketplace for buying and selling room essentials "
        "(study tables, desert coolers, bicycles, academic textbooks, electronics) directly between peers, powered by an asynchronous "
        "machine learning recommendation microservice."
    )
    p = doc.add_paragraph(
        "The application is structured into four decoupled, autonomous tiers: a high-performance Java 21 / Spring Boot 3.3 REST API backend, "
        "a normalized MySQL 8.0 relational database with 12 ACID-compliant tables, an asynchronous Python 3.11 / Flask machine learning "
        "recommendation engine executing Scikit-learn TF-IDF vectorization and cosine similarity, and an ultra-responsive, zero-dependency "
        "vanilla HTML5/CSS3/ES6 frontend modeled after top-tier classifieds (OLX and Amazon)."
    )

    doc.add_heading("2. Comprehensive Technology Stack", level=1)
    p = doc.add_paragraph("The technical stack was chosen to eliminate heavy client-side framework bloat while providing rock-solid enterprise scalability:")

    # Tech stack table
    table_ts = doc.add_table(rows=1, cols=4)
    table_ts.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_ts.rows[0].cells
    hdr_titles = ["Layer / Subsystem", "Primary Technologies", "Specific Version", "Key Architectural Purpose"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "002F34")
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(9.5)
        set_cell_margins(hdr_cells[i], 120, 120, 140, 140)

    ts_data = [
        ("Frontend Web App", "Vanilla HTML5, Modern CSS3 (Grid & Flexbox), ES6+ JavaScript, Chart.js", "HTML5 / ES2022", "High-speed, framework-free client rendering (OLX & Amazon UX), responsive viewports from 320px to 1920px, interactive room selector, instant DOM updates."),
        ("Backend REST API", "Java, Spring Boot, Spring Security, Spring Data JPA, Hibernate, HikariCP, JJWT", "Java 21 / Spring Boot 3.3.0", "Core transactional microservice, stateless JWT token authentication, role-based access control (RBAC), ACID booking transactions, REST API contracts."),
        ("ML Recommender", "Python, Flask, Scikit-learn, NumPy, Pandas, Pickle, CORS", "Python 3.11 / Flask 3.0", "Asynchronous content-based recommendations using TF-IDF vectorization and cosine similarity over property amenities and product descriptions."),
        ("Relational Database", "MySQL Community Server, InnoDB Engine, Docker Containerization", "MySQL 8.0.36", "Normalized relational store (12 tables in 3NF/BCNF), foreign key cascades, high-cardinality indexing on location and category fields, data integrity."),
        ("Testing & Quality Assurance", "JUnit 5, Mockito, Puppeteer (Headless Chrome), Python Requests, AssertJ", "JUnit 5.10 / Node 20", "7-suite automated verification pipeline: unit tests, cross-viewport audit (320px-1920px), link integrity, AI artifact scanner, cloud audit, smoke tests."),
        ("DevOps & Deployment", "Docker, Docker Compose, Render Cloud, Vercel, Aiven Cloud MySQL", "Docker 26.0 / Render / Vercel", "Zero-cost distributed cloud topology with multi-stage container builds, automatic environment variable binding, and continuous integration.")
    ]

    for row_data in ts_data:
        row_cells = table_ts.add_row().cells
        for col_idx, val in enumerate(row_data):
            row_cells[col_idx].text = val
            p = row_cells[col_idx].paragraphs[0]
            p.runs[0].font.size = Pt(9)
            set_cell_margins(row_cells[col_idx], 80, 80, 100, 100)
            if col_idx == 0:
                p.runs[0].font.bold = True
                set_cell_background(row_cells[col_idx], "F4F6F8")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    doc.add_heading("3. Equal Team Work Allocation Matrix (25% Per Member)", level=1)
    p = doc.add_paragraph(
        "To ensure balanced accountability, fair technical evaluation, and complete mastery during academic examination, "
        "the StayMart system has been partitioned into four equally weighted domains (25% each). Each domain has distinct "
        "deliverables, design patterns, algorithmic implementations, and test suites."
    )

    # Work allocation summary table
    table_wa = doc.add_table(rows=1, cols=5)
    table_wa.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_wa.rows[0].cells
    hdr_titles = ["Team Member", "Role Title", "Allocated Domain", "Share", "Core Deliverables & Files"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "002F34")
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(9.5)
        set_cell_margins(hdr_cells[i], 120, 120, 140, 140)

    wa_data = [
        ("Divyansh Joshi", "Lead Backend Developer & Security Architect", "Spring Boot Core Services, Security & REST APIs", "25%", "Auth & JWT Security, Role-Based Access Control, Property & Booking Service Layers, JPA Entities, DataSeeder."),
        ("Gorav Kumar", "Database Administrator & Machine Learning Engineer", "Relational Database Engineering & ML Microservice", "25%", "12-Table MySQL 3NF/BCNF Schema, SQL DDL/Seed scripts, Python Flask Microservice, Scikit-learn TF-IDF Recommender, Database Fallback Engine."),
        ("Gorav Bhatt", "Lead Frontend Developer & UI/UX Designer", "Design System, Public Portals & Accommodation Discovery", "25%", "OLX/Amazon Design System, 26+ Responsive HTML/CSS/JS Pages, Faceted Search & Filtering, Room Selection Widget, Campus Re-Commerce UI."),
        ("Divyanshu Mehra", "Systems Integration, DevOps & QA Lead", "P2P Messaging, Admin Analytics & Automated QA Pipeline", "25%", "Real-time Student-Host Chat System, Admin Analytics Console (Chart.js), Docker Infrastructure, 7-Suite Master Verification Pipeline (283 Tests).")
    ]

    for row_data in wa_data:
        row_cells = table_wa.add_row().cells
        for col_idx, val in enumerate(row_data):
            row_cells[col_idx].text = val
            p = row_cells[col_idx].paragraphs[0]
            p.runs[0].font.size = Pt(9)
            set_cell_margins(row_cells[col_idx], 80, 80, 100, 100)
            if col_idx == 0:
                p.runs[0].font.bold = True
                set_cell_background(row_cells[col_idx], "EBF3F5")

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Detailed sections per member
    members = [
        {
            "name": "Divyansh Joshi",
            "role": "Lead Backend Developer & Security Architect",
            "domain": "Spring Boot 3.3 Core REST APIs, JWT Security, RBAC & Transactional Services",
            "share": "25% of Project Scope",
            "modules": [
                "Stateless JWT Authentication Engine: Developed JwtTokenProvider and JwtAuthenticationFilter handling HMAC-SHA256 signature generation, claims extraction, token expiration validation, and injecting Spring Security authentication contexts.",
                "Role-Based Access Control (RBAC): Implemented fine-grained method security supporting three distinct roles: ROLE_STUDENT (browsing, booking, purchasing, wishlist), ROLE_CARETAKER (host listing management, room vacancy toggling), and ROLE_ADMIN (platform moderation, analytics access).",
                "Domain Entity Modeling & Hibernate Mapping: Authored core JPA entities with bidirectional relationships, cascade types, lazy fetching, and temporal auditing (@CreationTimestamp): User, Property, Room, Booking, Wishlist, Category, Location.",
                "Accommodation & Booking Service Layer: Engineered transactional business logic ensuring atomic booking operations: validating room capacity, calculating total rent/security deposits, updating availability status, and preventing duplicate double-bookings under concurrent requests.",
                "Automated Data Seeder: Built DataSeeder.java implementing ApplicationRunner to automatically bootstrap administrative credentials (admin@staymart.com), verified test caretakers, student profiles, and standard category taxonomies upon cold boot."
            ],
            "files": [
                "src/main/java/com/staymart/security/JwtTokenProvider.java",
                "src/main/java/com/staymart/security/JwtAuthenticationFilter.java",
                "src/main/java/com/staymart/security/SecurityConfig.java",
                "src/main/java/com/staymart/entity/User.java, Property.java, Room.java, Booking.java",
                "src/main/java/com/staymart/controller/AuthController.java, PropertyController.java, BookingController.java",
                "src/main/java/com/staymart/service/PropertyService.java, BookingService.java",
                "src/main/java/com/staymart/config/DataSeeder.java"
            ],
            "viva_questions": [
                ("Q: Why did you choose stateless JWT over traditional HTTP session cookies?", 
                 "A: In a multi-tier microservice architecture, stateless JWT eliminates server-side session memory overhead and allows seamless horizontal scaling across cloud instances without requiring sticky sessions or a shared Redis session store."),
                ("Q: How does Spring Security intercept requests and authenticate tokens?", 
                 "A: JwtAuthenticationFilter extends OncePerRequestFilter. It intercepts the HTTP Authorization header, strips the 'Bearer ' prefix, verifies the signature using the secret key via JJWT, extracts username/roles, and sets the UsernamePasswordAuthenticationToken into SecurityContextHolder."),
                ("Q: How do you prevent double-booking of accommodation rooms?", 
                 "A: In BookingService, we wrap the reservation in a @Transactional boundary. We verify the room's current vacancy and capacity before persisting the booking record and decrementing availability atomically.")
            ]
        },
        {
            "name": "Gorav Kumar",
            "role": "Database Administrator & Machine Learning Engineer",
            "domain": "MySQL Relational Database Engineering, Normalization & Python ML Recommender Microservice",
            "share": "25% of Project Scope",
            "modules": [
                "Relational Schema Design & Normalization: Designed and implemented the complete 12-table MySQL relational database adhering to Boyce-Codd Normal Form (BCNF) and 3NF, eliminating data redundancy and update anomalies.",
                "Data Integrity & Indexing Architecture: Enforced referential integrity using FOREIGN KEY constraints with ON DELETE CASCADE / RESTRICT actions; constructed compound indexes on high-traffic filter columns (city, category_id, is_active, price) to maintain sub-50ms query latency.",
                "SQL DDL & Authentic Regional Seeding: Authored database/01_schema.sql, 02_seed.sql, and 03_seed_listings.sql containing realistic student accommodations around Graphic Era Hill University (Clement Town), UPES (Bidholi/Kandoli), DIT, and Roorkee, plus campus products.",
                "Python Flask Machine Learning Microservice: Architected ml-service/app.py and ml-service/recommender.py serving content-based recommendations over lightweight HTTP REST endpoints on port 5000.",
                "TF-IDF & Cosine Similarity Engine: Engineered an intelligent feature extractor combining title, description, amenities (Wi-Fi, RO water, power backup, attached washroom), and location strings into unified corpus vectors; computed cosine similarity matrices via Scikit-learn.",
                "Model Serialization & Automated Database Fallback: Pickled vectorizers (property_tfidf.pkl, product_tfidf.pkl) for instantaneous sub-10ms startup; engineered a resilient SQL-based similarity fallback in Spring Boot (RecommendationService) that automatically activates if the ML service is offline."
            ],
            "files": [
                "database/01_schema.sql (12 normalized tables DDL)",
                "database/02_seed.sql (Locations, categories, users, base listings)",
                "database/03_seed_listings.sql (Rich Uttarakhand campus listings & products)",
                "ml-service/app.py (Flask microservice application & endpoints)",
                "ml-service/recommender.py (TF-IDF vectorization & Cosine similarity computation)",
                "src/main/java/com/staymart/service/RecommendationService.java (Resilient fallback coordinator)"
            ],
            "viva_questions": [
                ("Q: Explain the mathematical intuition behind TF-IDF in StayMart.", 
                 "A: Term Frequency (TF) measures how frequently a term (e.g. 'AC', 'Attached Washroom', 'Clement Town') appears in a listing. Inverse Document Frequency (IDF) discounts ubiquitous words (e.g. 'room', 'hostel') so that distinctive amenities receive higher vector weight when calculating cosine similarity."),
                ("Q: What happens if the Python ML microservice crashes or is down during user requests?", 
                 "A: We built a high-availability fallback in RecommendationService.java using RestTemplate with a 2-second connection timeout. If the microservice fails or times out, the backend automatically catches the exception and executes an optimized SQL fallback querying identical categories and location tags, providing 100% uptime with zero user disruption."),
                ("Q: How did you ensure 3NF compliance in the database?", 
                 "A: All tables have a designated primary key, every non-key attribute is fully functionally dependent on the primary key (2NF), and there are no transitive dependencies (3NF). For example, location details (city, state, campus zone) are isolated in a separate locations table rather than duplicated in properties.")
            ]
        },
        {
            "name": "Gorav Bhatt",
            "role": "Lead Frontend Developer & UI/UX Designer",
            "domain": "Design System Tokens, Responsive Multi-Device UX & Core Accommodation/Marketplace Portals",
            "share": "25% of Project Scope",
            "modules": [
                "Commercial Design System Architecture: Engineered a high-contrast, modern visual design system inspired by leading classified interfaces (OLX and Amazon), establishing CSS custom property design tokens for colors (--primary: #002f34, --accent: #ffce32, --surface: #ffffff), fluid typography, elevation shadows, and micro-interactions.",
                "Multi-Viewport Responsive Engineering: Architected 26+ HTML5/CSS3 pages guaranteeing strict zero-horizontal-overflow responsiveness across 6 device breakpoints (320px mobile up to 1920px 4K ultrawide monitors), fully passing automated Headless Chrome viewport audits.",
                "Public Discovery Portal (index.html): Built an engaging landing page featuring institutional campus chips (GEHU, UPES, DIT, Roorkee), search bar autocomplete, category carousels, and recent student listing grids.",
                "Faceted Accommodation Search & Filtering (properties.html): Developed dynamic client-side filtering supporting instant query evaluation across price range sliders, room type (Single, Double, Flat, PG), gender segregation (Boys, Girls, Co-ed), and amenity tags.",
                "Interactive Listing Detail Experience (property-detail.html): Implemented multi-image galleries with modal lightbox zoom, host verification badges, interactive room selection widgets with dynamic price calculations, and direct caretaker contact triggers.",
                "Campus Re-Commerce Marketplace (products.html, product-detail.html): Built dedicated student product classifieds featuring condition ratings (Like New, Good, Fair), price bargaining tags, and immediate wishlist bookmarking."
            ],
            "files": [
                "frontend/css/global.css (Core design system tokens & layout utilities)",
                "frontend/css/properties.css, frontend/css/products.css",
                "frontend/index.html (Landing page & campus discovery)",
                "frontend/properties.html & frontend/js/properties.js (Faceted accommodation portal)",
                "frontend/property-detail.html & frontend/js/property-detail.js (Room selector & gallery)",
                "frontend/products.html & frontend/product-detail.html (Student marketplace catalog)"
            ],
            "viva_questions": [
                ("Q: Why did you decide to use Vanilla JavaScript and CSS instead of React or Angular?", 
                 "A: In student rental platforms where network connectivity in hilly areas of Uttarakhand can be limited (2G/3G speeds), eliminating client-side framework bundles (React/Vue/Angular) reduces page weight by 80%, providing sub-second Time to Interactive (TTI), instant DOM rendering, and zero build tool fragility."),
                ("Q: How does the interactive room selection widget work on the property detail page?", 
                 "A: When the user selects a room option (e.g. 'Single Room with Balcony'), the JavaScript event listener dynamically parses the selected room's data attributes, recalculates the total monthly rent plus refundable security deposit, validates availability against capacity, and updates the booking form payload."),
                ("Q: How did you ensure consistent design tokens across 26 pages?", 
                 "A: By defining standard CSS variables in global.css under the :root selector. All page-specific stylesheets reference these variables (e.g. var(--primary), var(--radius-md)), guaranteeing uniform branding, spacing, and transitions across the entire site.")
            ]
        },
        {
            "name": "Divyanshu Mehra",
            "role": "Systems Integration, DevOps & QA Lead",
            "domain": "Peer-to-Peer Messaging, Admin Moderation Console, Docker DevOps & 7-Suite Automated QA Pipeline",
            "share": "25% of Project Scope",
            "modules": [
                "Peer-to-Peer Real-Time Student-Host Messaging: Architected the complete messaging subsystem (chat.html, js/chat.js, ChatController, ChatService, and messages table) enabling direct, zero-brokerage negotiations between students and verified property caretakers with unread badges and active conversation threads.",
                "Administrative Moderation & Analytics Console (admin.html): Developed a comprehensive management console featuring live Chart.js visualizations (monthly booking trends, revenue distribution, category breakdown), moderation queues for unverified listings, user suspension toggles, and platform KPI tiles.",
                "Docker Containerization & Multi-Service Orchestration: Engineered the multi-stage production Dockerfile and orchestration scripts (scripts/start-all.ps1, scripts/stop-all.ps1) managing the containerized MySQL 8.0 database, Java backend, and Python ML service with healthcheck monitoring.",
                "Unified 7-Suite Automated Verification Pipeline (scripts/run_all_verifications.py): Built the master test automation harness executing 283 tests across 7 verification suites with 100% pass rate, zero regressions, and automated JSON reporting.",
                "Adversarial Viewport & Smoke Test Automation: Authored scripts/run_viewport_tests.js (Puppeteer headless Chrome auditing 30 page/viewport combinations) and scripts/run_smoke_tests.py (97 multi-tier API contract tests verifying reachability, authentication, and error handling).",
                "Academic Report Compilation & Formatting: Engineered the 3-pass PDF report compilation engine (scripts/compile_report_pdf.py) producing the exact 80-page, GEHU-compliant academic project report with Roman/Arabic two-tier numbering and automated TOC synchronization."
            ],
            "files": [
                "frontend/chat.html & frontend/js/chat.js (Peer-to-peer messaging interface)",
                "frontend/admin.html & frontend/js/admin.js (Administrative analytics console)",
                "src/main/java/com/staymart/controller/ChatController.java, AdminController.java",
                "scripts/run_all_verifications.py (Master 7-suite verification runner)",
                "scripts/run_viewport_tests.js & scripts/run_smoke_tests.py",
                "scripts/start-all.ps1 & scripts/stop-all.ps1 (Daemon orchestration)",
                "scripts/compile_report_pdf.py (80-Page GEHU academic report compiler)"
            ],
            "viva_questions": [
                ("Q: How does the peer-to-peer messaging system handle authentication and privacy?", 
                 "A: Every chat message request passes through JwtAuthenticationFilter. ChatService validates that the authenticated user is either the sender or receiver of the conversation thread, preventing unauthorized eavesdropping, and stores messages with timestamps and read receipts in MySQL."),
                ("Q: Explain what your 7-Suite Automated Verification Pipeline tests.", 
                 "A: It executes 283 automated checks across 7 critical domains: (1) JUnit 5 backend tests, (2) Puppeteer viewport rendering (320px-1920px), (3) DOM navigation link integrity, (4) AI artifact scanner, (5) Cloud deployment manifests, (6) 80-page PDF report compilation, and (7) Multi-tier API smoke testing."),
                ("Q: How is the application deployed to cloud environments without incurring costs?", 
                 "A: We designed a decoupled zero-cost architecture: the vanilla frontend is deployed to Vercel (free static tier with CDN), the Spring Boot backend and Flask ML microservice run as Docker containers on Render's free tier, and MySQL is provisioned via Aiven Free MySQL cloud database.")
            ]
        }
    ]

    for m in members:
        doc.add_heading(f"4.{members.index(m)+1} Member Profile: {m['name']} (25%)", level=2)
        
        p = doc.add_paragraph()
        run = p.add_run(f"Assigned Role: {m['role']}\nAllocated Domain: {m['domain']}\nWorkload Contribution: {m['share']}")
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x00, 0x2F, 0x34)
        p.paragraph_format.space_after = Pt(8)

        doc.add_heading("Detailed Technical Contributions & Owned Modules:", level=3)
        for mod in m['modules']:
            doc.add_paragraph(mod, style='List Bullet')

        doc.add_heading("Key Source Files & Artifacts Owned:", level=3)
        for f in m['files']:
            doc.add_paragraph(f, style='List Bullet')

        doc.add_heading("Viva Voce & Technical Defense Preparation (Questions & Model Answers):", level=3)
        for q, a in m['viva_questions']:
            p_q = doc.add_paragraph()
            r_q = p_q.add_run(q)
            r_q.font.bold = True
            r_q.font.color.rgb = RGBColor(0x9E, 0x5B, 0x00) # Amber dark
            p_a = doc.add_paragraph()
            r_a = p_a.add_run(a)
            r_a.font.italic = False
            p_a.paragraph_format.space_after = Pt(8)

    doc.add_heading("5. Verification and Quality Assurance Matrix", level=1)
    p = doc.add_paragraph(
        "To satisfy rigorous university engineering standards, the team executed an exhaustive automated testing regimen "
        "covering unit, integration, UI viewport, and microservice contract boundaries. All 283 tests pass with 0 failures:"
    )

    table_qa = doc.add_table(rows=1, cols=4)
    table_qa.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_qa.rows[0].cells
    hdr_titles = ["Verification Suite", "Scope / Tooling", "Tests Executed", "Result & Status"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "002F34")
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(9.5)
        set_cell_margins(hdr_cells[i], 120, 120, 140, 140)

    qa_data = [
        ("1. Spring Boot Backend Unit & Integration Tests", "JUnit 5, Mockito, Security Filter & Entity Tests", "13", "13 / 13 PASSED (100%)"),
        ("2. Headless Chrome Multi-Viewport Audit", "Puppeteer (320px, 480px, 768px, 1024px, 1440px, 1920px)", "30", "30 / 30 PASSED (100%)"),
        ("3. Navigation & DOM Link Integrity Audit", "Python HTML DOM traversal, 404 & redirect detection", "8", "8 / 8 PASSED (100%)"),
        ("4. Adversarial AI Artifact & Pattern Scanner", "Python AST & Regex Scanner across 87 source files", "87", "87 / 87 PASSED (100%)"),
        ("5. Cloud Deployment & Manifest Security Audit", "Environment variable auditing, YAML validation", "47", "47 / 47 PASSED (100%)"),
        ("6. Academic PDF Report Compiler", "Headless Chrome 3-Pass Compiler (80 Pages, GEHU Specs)", "1", "1 / 1 PASSED (80 Pages)"),
        ("7. Multi-Tier API Smoke Test Suite", "Python Requests probing Spring Boot (:8080) & Flask (:5000)", "97", "97 / 97 PASSED (100%)")
    ]

    for row_data in qa_data:
        row_cells = table_qa.add_row().cells
        for col_idx, val in enumerate(row_data):
            row_cells[col_idx].text = val
            p = row_cells[col_idx].paragraphs[0]
            p.runs[0].font.size = Pt(9)
            set_cell_margins(row_cells[col_idx], 80, 80, 100, 100)
            if col_idx == 3:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(0x00, 0x80, 0x00)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    doc.add_heading("6. Project Run and Demonstration Instructions", level=1)
    p = doc.add_paragraph(
        "The complete multi-service application can be started or stopped instantaneously via automated PowerShell scripts:"
    )
    p = doc.add_paragraph(
        "1. Start All Services:\n"
        "   powershell -File scripts/start-all.ps1 -Restart -Wait\n"
        "   - MySQL Container: 127.0.0.1:3306\n"
        "   - Spring Boot Backend API: http://localhost:8080/api\n"
        "   - Swagger UI Documentation: http://localhost:8080/swagger-ui.html\n"
        "   - Python Flask ML Service: http://localhost:5000/health\n"
        "   - Frontend Web Application: http://localhost:5500\n\n"
        "2. Stop All Services:\n"
        "   powershell -File scripts/stop-all.ps1\n\n"
        "3. Demo Credentials:\n"
        "   - Administrator: admin@staymart.com / Admin@123\n"
        "   - Verified Student: divyanshu@gehu.ac.in / Password@123"
    )

    doc.save(DOCX_OUTPUT)
    print(f"[SUCCESS] Generated DOCX at: {DOCX_OUTPUT}")

def create_markdown():
    md = """# STAYMART: SMART STUDENT HOUSING AND CAMPUS MARKETPLACE
## Team Work Allocation, Architectural Framework, Tech Stack & Implementation Guide

- **Degree:** Bachelor of Computer Applications (BCA)
- **Department:** School of Computing, Graphic Era Hill University (GEHU), Dehradun
- **Academic Year:** 2026
- **Faculty Mentor:** Ms. Tabish Rao
- **Team Members:** Divyansh Joshi, Gorav Kumar, Gorav Bhatt, Divyanshu Mehra

---

## 1. Executive Project Summary

**StayMart** is a production-grade, distributed web platform specifically engineered to address the critical living and commerce challenges faced by tertiary students across university clusters in Uttarakhand (including Dehradun, Rishikesh, and Roorkee). The platform bridges two interconnected student requirements:

1. **Zero-Brokerage Student Accommodation:** Finding verified, affordable rental accommodation with room-level vacancy tracking, direct host communication, and transparent rental agreements.
2. **Campus Re-Commerce Marketplace:** An intra-campus marketplace for buying and selling room essentials (study tables, desert coolers, bicycles, academic textbooks, electronics) directly between peers.
3. **Machine Learning Intelligence:** An asynchronous recommendation microservice computing content similarity via Scikit-learn TF-IDF vectorization and cosine similarity, backed by automated database fallbacks.

The application is structured into four decoupled, autonomous tiers:
- **Java 21 / Spring Boot 3.3 REST API backend**
- **Normalized MySQL 8.0 relational database (12 tables in 3NF/BCNF)**
- **Python 3.11 / Flask machine learning microservice**
- **Ultra-responsive vanilla HTML5, CSS3, and ES6+ JavaScript frontend (OLX & Amazon UX)**

---

## 2. Comprehensive Technology Stack Breakdown

| Layer / Subsystem | Primary Technologies | Specific Version | Key Architectural Purpose |
|---|---|---|---|
| **Frontend Web App** | Vanilla HTML5, Modern CSS3 (Grid & Flexbox), ES6+ JavaScript, Chart.js | HTML5 / ES2022 | High-speed, framework-free client rendering (OLX & Amazon UX), responsive viewports from 320px to 1920px, interactive room selector, instant DOM updates. |
| **Backend REST API** | Java, Spring Boot, Spring Security, Spring Data JPA, Hibernate, HikariCP, JJWT | Java 21 / Spring Boot 3.3.0 | Core transactional microservice, stateless JWT token authentication, role-based access control (RBAC), ACID booking transactions, REST API contracts. |
| **ML Recommender** | Python, Flask, Scikit-learn, NumPy, Pandas, Pickle, CORS | Python 3.11 / Flask 3.0 | Asynchronous content-based recommendations using TF-IDF vectorization and cosine similarity over property amenities and product descriptions. |
| **Relational Database** | MySQL Community Server, InnoDB Engine, Docker Containerization | MySQL 8.0.36 | Normalized relational store (12 tables in 3NF/BCNF), foreign key cascades, high-cardinality indexing on location and category fields, data integrity. |
| **Testing & QA** | JUnit 5, Mockito, Puppeteer (Headless Chrome), Python Requests, AssertJ | JUnit 5.10 / Node 20 | 7-suite automated verification pipeline: unit tests, cross-viewport audit (320px-1920px), link integrity, AI artifact scanner, cloud audit, smoke tests. |
| **DevOps & Cloud** | Docker, Docker Compose, Render Cloud, Vercel, Aiven Cloud MySQL | Docker 26.0 / Render / Vercel | Zero-cost distributed cloud topology with multi-stage container builds, automatic environment variable binding, and continuous integration. |

---

## 3. Equal Team Work Allocation Matrix (25% Per Member)

The project scope has been divided into four equal technical areas (25% each):

| Team Member | Role Title | Allocated Domain | Share | Core Deliverables & Files |
|---|---|---|:---:|---|
| **Divyansh Joshi** | Lead Backend Developer & Security Architect | Spring Boot Core Services, Security & REST APIs | **25%** | Auth & JWT Security, Role-Based Access Control, Property & Booking Service Layers, JPA Entities, DataSeeder. |
| **Gorav Kumar** | Database Administrator & Machine Learning Engineer | Relational Database Engineering & ML Microservice | **25%** | 12-Table MySQL 3NF/BCNF Schema, SQL DDL/Seed scripts, Python Flask Microservice, Scikit-learn TF-IDF Recommender, Database Fallback Engine. |
| **Gorav Bhatt** | Lead Frontend Developer & UI/UX Designer | Design System, Public Portals & Accommodation Discovery | **25%** | OLX/Amazon Design System, 26+ Responsive HTML/CSS/JS Pages, Faceted Search & Filtering, Room Selection Widget, Campus Re-Commerce UI. |
| **Divyanshu Mehra** | Systems Integration, DevOps & QA Lead | P2P Messaging, Admin Analytics & Automated QA Pipeline | **25%** | Real-time Student-Host Chat System, Admin Analytics Console (Chart.js), Docker Infrastructure, 7-Suite Master Verification Pipeline (283 Tests). |

---

## 4. In-Depth Member Breakdown & Viva Preparation Guide

### 4.1 Divyansh Joshi (25%) — Lead Backend Developer & Security Architect
- **Assigned Domain:** Spring Boot 3.3 Core REST APIs, JWT Security, RBAC & Transactional Services
- **Detailed Technical Responsibilities:**
  1. **Stateless JWT Authentication Engine:** Developed `JwtTokenProvider` and `JwtAuthenticationFilter` handling HMAC-SHA256 signature generation, claims extraction, token expiration validation, and injecting Spring Security authentication contexts.
  2. **Role-Based Access Control (RBAC):** Implemented fine-grained method security supporting three distinct roles: `ROLE_STUDENT` (browsing, booking, purchasing, wishlist), `ROLE_CARETAKER` (host listing management, room vacancy toggling), and `ROLE_ADMIN` (platform moderation, analytics access).
  3. **Domain Entity Modeling & Hibernate Mapping:** Authored core JPA entities with bidirectional relationships, cascade types, lazy fetching, and temporal auditing (`@CreationTimestamp`): `User`, `Property`, `Room`, `Booking`, `Wishlist`, `Category`, `Location`.
  4. **Accommodation & Booking Service Layer:** Engineered transactional business logic ensuring atomic booking operations: validating room capacity, calculating total rent/security deposits, updating availability status, and preventing duplicate double-bookings under concurrent requests.
  5. **Automated Data Seeder:** Built `DataSeeder.java` implementing `ApplicationRunner` to automatically bootstrap administrative credentials (`admin@staymart.com`), verified test caretakers, student profiles, and standard category taxonomies upon cold boot.
- **Key Source Code Files:**
  - `src/main/java/com/staymart/security/JwtTokenProvider.java`
  - `src/main/java/com/staymart/security/JwtAuthenticationFilter.java`
  - `src/main/java/com/staymart/security/SecurityConfig.java`
  - `src/main/java/com/staymart/entity/User.java`, `Property.java`, `Room.java`, `Booking.java`
  - `src/main/java/com/staymart/controller/AuthController.java`, `PropertyController.java`, `BookingController.java`
  - `src/main/java/com/staymart/service/PropertyService.java`, `BookingService.java`
  - `src/main/java/com/staymart/config/DataSeeder.java`
- **Viva Voce Preparation & Model Answers:**
  - **Q: Why did you choose stateless JWT over traditional HTTP session cookies?**  
    *A: In a multi-tier microservice architecture, stateless JWT eliminates server-side session memory overhead and allows seamless horizontal scaling across cloud instances without requiring sticky sessions or a shared Redis session store.*
  - **Q: How does Spring Security intercept requests and authenticate tokens?**  
    *A: `JwtAuthenticationFilter` extends `OncePerRequestFilter`. It intercepts the HTTP `Authorization` header, strips the `Bearer ` prefix, verifies the signature using the secret key via JJWT, extracts username/roles, and sets the `UsernamePasswordAuthenticationToken` into `SecurityContextHolder`.*
  - **Q: How do you prevent double-booking of accommodation rooms?**  
    *A: In `BookingService`, we wrap the reservation in a `@Transactional` boundary. We verify the room's current vacancy and capacity before persisting the booking record and decrementing availability atomically.*

---

### 4.2 Gorav Kumar (25%) — Database Administrator & Machine Learning Engineer
- **Assigned Domain:** MySQL Relational Database Engineering, Normalization & Python ML Recommender Microservice
- **Detailed Technical Responsibilities:**
  1. **Relational Schema Design & Normalization:** Designed and implemented the complete 12-table MySQL relational database adhering to Boyce-Codd Normal Form (BCNF) and 3NF, eliminating data redundancy and update anomalies.
  2. **Data Integrity & Indexing Architecture:** Enforced referential integrity using `FOREIGN KEY` constraints with `ON DELETE CASCADE` / `RESTRICT` actions; constructed compound indexes on high-traffic filter columns (`city`, `category_id`, `is_active`, `price`) to maintain sub-50ms query latency.
  3. **SQL DDL & Authentic Regional Seeding:** Authored `database/01_schema.sql`, `02_seed.sql`, and `03_seed_listings.sql` containing realistic student accommodations around Graphic Era Hill University (Clement Town), UPES (Bidholi/Kandoli), DIT, and Roorkee, plus campus products.
  4. **Python Flask Machine Learning Microservice:** Architected `ml-service/app.py` and `ml-service/recommender.py` serving content-based recommendations over lightweight HTTP REST endpoints on port 5000.
  5. **TF-IDF & Cosine Similarity Engine:** Engineered an intelligent feature extractor combining title, description, amenities (Wi-Fi, RO water, power backup, attached washroom), and location strings into unified corpus vectors; computed cosine similarity matrices via Scikit-learn.
  6. **Model Serialization & Automated Database Fallback:** Pickled vectorizers (`property_tfidf.pkl`, `product_tfidf.pkl`) for instantaneous sub-10ms startup; engineered a resilient SQL-based similarity fallback in Spring Boot (`RecommendationService`) that automatically activates if the ML service is offline.
- **Key Source Code Files:**
  - `database/01_schema.sql` (12 normalized tables DDL)
  - `database/02_seed.sql` (Locations, categories, users, base listings)
  - `database/03_seed_listings.sql` (Rich Uttarakhand campus listings & products)
  - `ml-service/app.py` (Flask microservice application & endpoints)
  - `ml-service/recommender.py` (TF-IDF vectorization & Cosine similarity computation)
  - `src/main/java/com/staymart/service/RecommendationService.java` (Resilient fallback coordinator)
- **Viva Voce Preparation & Model Answers:**
  - **Q: Explain the mathematical intuition behind TF-IDF in StayMart.**  
    *A: Term Frequency (TF) measures how frequently a term (e.g. 'AC', 'Attached Washroom', 'Clement Town') appears in a listing. Inverse Document Frequency (IDF) discounts ubiquitous words (e.g. 'room', 'hostel') so that distinctive amenities receive higher vector weight when calculating cosine similarity.*
  - **Q: What happens if the Python ML microservice crashes or is down during user requests?**  
    *A: We built a high-availability fallback in `RecommendationService.java` using `RestTemplate` with a 2-second connection timeout. If the microservice fails or times out, the backend automatically catches the exception and executes an optimized SQL fallback querying identical categories and location tags, providing 100% uptime with zero user disruption.*
  - **Q: How did you ensure 3NF compliance in the database?**  
    *A: All tables have a designated primary key, every non-key attribute is fully functionally dependent on the primary key (2NF), and there are no transitive dependencies (3NF). For example, location details (city, state, campus zone) are isolated in a separate `locations` table rather than duplicated in `properties`.*

---

### 4.3 Gorav Bhatt (25%) — Lead Frontend Developer & UI/UX Designer
- **Assigned Domain:** Design System Tokens, Responsive Multi-Device UX & Core Accommodation/Marketplace Portals
- **Detailed Technical Responsibilities:**
  1. **Commercial Design System Architecture:** Engineered a high-contrast, modern visual design system inspired by leading classified interfaces (OLX and Amazon), establishing CSS custom property design tokens for colors (`--primary: #002f34`, `--accent: #ffce32`, `--surface: #ffffff`), fluid typography, elevation shadows, and micro-interactions.
  2. **Multi-Viewport Responsive Engineering:** Architected 26+ HTML5/CSS3 pages guaranteeing strict zero-horizontal-overflow responsiveness across 6 device breakpoints (320px mobile up to 1920px 4K ultrawide monitors), fully passing automated Headless Chrome viewport audits.
  3. **Public Discovery Portal (index.html):** Built an engaging landing page featuring institutional campus chips (GEHU, UPES, DIT, Roorkee), search bar autocomplete, category carousels, and recent student listing grids.
  4. **Faceted Accommodation Search & Filtering (properties.html):** Developed dynamic client-side filtering supporting instant query evaluation across price range sliders, room type (Single, Double, Flat, PG), gender segregation (Boys, Girls, Co-ed), and amenity tags.
  5. **Interactive Listing Detail Experience (property-detail.html):** Implemented multi-image galleries with modal lightbox zoom, host verification badges, interactive room selection widgets with dynamic price calculations, and direct caretaker contact triggers.
  6. **Campus Re-Commerce Marketplace (products.html, product-detail.html):** Built dedicated student product classifieds featuring condition ratings (Like New, Good, Fair), price bargaining tags, and immediate wishlist bookmarking.
- **Key Source Code Files:**
  - `frontend/css/global.css` (Core design system tokens & layout utilities)
  - `frontend/css/properties.css`, `frontend/css/products.css`
  - `frontend/index.html` (Landing page & campus discovery)
  - `frontend/properties.html` & `frontend/js/properties.js` (Faceted accommodation portal)
  - `frontend/property-detail.html` & `frontend/js/property-detail.js` (Room selector & gallery)
  - `frontend/products.html` & `frontend/product-detail.html` (Student marketplace catalog)
- **Viva Voce Preparation & Model Answers:**
  - **Q: Why did you decide to use Vanilla JavaScript and CSS instead of React or Angular?**  
    *A: In student rental platforms where network connectivity in hilly areas of Uttarakhand can be limited (2G/3G speeds), eliminating client-side framework bundles (React/Vue/Angular) reduces page weight by 80%, providing sub-second Time to Interactive (TTI), instant DOM rendering, and zero build tool fragility.*
  - **Q: How does the interactive room selection widget work on the property detail page?**  
    *A: When the user selects a room option (e.g. 'Single Room with Balcony'), the JavaScript event listener dynamically parses the selected room's data attributes, recalculates the total monthly rent plus refundable security deposit, validates availability against capacity, and updates the booking form payload.*
  - **Q: How did you ensure consistent design tokens across 26 pages?**  
    *A: By defining standard CSS variables in `global.css` under the `:root` selector. All page-specific stylesheets reference these variables (e.g. `var(--primary)`, `var(--radius-md)`), guaranteeing uniform branding, spacing, and transitions across the entire site.*

---

### 4.4 Divyanshu Mehra (25%) — Systems Integration, DevOps & QA Lead
- **Assigned Domain:** Peer-to-Peer Messaging, Admin Moderation Console, Docker DevOps & 7-Suite Automated QA Pipeline
- **Detailed Technical Responsibilities:**
  1. **Peer-to-Peer Real-Time Student-Host Messaging:** Architected the complete messaging subsystem (`chat.html`, `js/chat.js`, `ChatController`, `ChatService`, and `messages` table) enabling direct, zero-brokerage negotiations between students and verified property caretakers with unread badges and active conversation threads.
  2. **Administrative Moderation & Analytics Console (admin.html):** Developed a comprehensive management console featuring live Chart.js visualizations (monthly booking trends, revenue distribution, category breakdown), moderation queues for unverified listings, user suspension toggles, and platform KPI tiles.
  3. **Docker Containerization & Multi-Service Orchestration:** Engineered the multi-stage production `Dockerfile` and orchestration scripts (`scripts/start-all.ps1`, `scripts/stop-all.ps1`) managing the containerized MySQL 8.0 database, Java backend, and Python ML service with healthcheck monitoring.
  4. **Unified 7-Suite Automated Verification Pipeline (scripts/run_all_verifications.py):** Built the master test automation harness executing 283 tests across 7 verification suites with 100% pass rate, zero regressions, and automated JSON reporting.
  5. **Adversarial Viewport & Smoke Test Automation:** Authored `scripts/run_viewport_tests.js` (Puppeteer headless Chrome auditing 30 page/viewport combinations) and `scripts/run_smoke_tests.py` (97 multi-tier API contract tests verifying reachability, authentication, and error handling).
  6. **Academic Report Compilation & Formatting:** Engineered the 3-pass PDF report compilation engine (`scripts/compile_report_pdf.py`) producing the exact 80-page, GEHU-compliant academic project report with Roman/Arabic two-tier numbering and automated TOC synchronization.
- **Key Source Code Files:**
  - `frontend/chat.html` & `frontend/js/chat.js` (Peer-to-peer messaging interface)
  - `frontend/admin.html` & `frontend/js/admin.js` (Administrative analytics console)
  - `src/main/java/com/staymart/controller/ChatController.java`, `AdminController.java`
  - `scripts/run_all_verifications.py` (Master 7-suite verification runner)
  - `scripts/run_viewport_tests.js` & `scripts/run_smoke_tests.py`
  - `scripts/start-all.ps1` & `scripts/stop-all.ps1` (Daemon orchestration)
  - `scripts/compile_report_pdf.py` (80-Page GEHU academic report compiler)
- **Viva Voce Preparation & Model Answers:**
  - **Q: How does the peer-to-peer messaging system handle authentication and privacy?**  
    *A: Every chat message request passes through `JwtAuthenticationFilter`. `ChatService` validates that the authenticated user is either the sender or receiver of the conversation thread, preventing unauthorized eavesdropping, and stores messages with timestamps and read receipts in MySQL.*
  - **Q: Explain what your 7-Suite Automated Verification Pipeline tests.**  
    *A: It executes 283 automated checks across 7 critical domains: (1) JUnit 5 backend tests, (2) Puppeteer viewport rendering (320px-1920px), (3) DOM navigation link integrity, (4) AI artifact scanner, (5) Cloud deployment manifests, (6) 80-page PDF report compilation, and (7) Multi-tier API smoke testing.*
  - **Q: How is the application deployed to cloud environments without incurring costs?**  
    *A: We designed a decoupled zero-cost architecture: the vanilla frontend is deployed to Vercel (free static tier with CDN), the Spring Boot backend and Flask ML microservice run as Docker containers on Render's free tier, and MySQL is provisioned via Aiven Free MySQL cloud database.*

---

## 5. Master Automated Verification Matrix (283/283 Tests Passed)

| # | Verification Suite | Target Domain / Tooling | Tests Run | Status |
|---|---|---|:---:|:---:|
| 1 | **Spring Boot Backend Tests** | JUnit 5, Mockito, Security & Service Mocks | 13 | **PASS (13/13)** |
| 2 | **Headless Chrome Viewports** | Puppeteer (320px to 1920px viewports) | 30 | **PASS (30/30)** |
| 3 | **Navigation & Link Audit** | Python DOM Crawler (Zero 404 dead links) | 8 | **PASS (8/8)** |
| 4 | **AI Pattern & Security Scanner** | AST & Regex scan across 87 source files | 87 | **PASS (87/87)** |
| 5 | **Cloud Deployment Audit** | Environment bindings & Manifest validations | 47 | **PASS (47/47)** |
| 6 | **Academic PDF Report Compiler** | 3-Pass Headless Chrome Compiler (80 Pages) | 1 | **PASS (80 Pages)** |
| 7 | **Multi-Tier API Smoke Tests** | HTTP API contract tests (:8080 & :5000) | 97 | **PASS (97/97)** |
| **Total** | **Full Verification Pipeline** | **283 Automated Tests Across All Layers** | **283** | **100% PASS** |

---

## 6. How to Run and Demonstrate the System

### Starting All Services:
```powershell
powershell -File scripts/start-all.ps1 -Restart -Wait
```
- **Frontend App:** [http://localhost:5500](http://localhost:5500)
- **Backend REST API:** [http://localhost:8080/api](http://localhost:8080/api)
- **Swagger UI Console:** [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)
- **ML Recommender Health:** [http://localhost:5000/health](http://localhost:5000/health)
- **MySQL Database:** `127.0.0.1:3306` (Docker container `staymart-mysql`)

### Stopping All Services:
```powershell
powershell -File scripts/stop-all.ps1
```

### Pre-configured Login Accounts:
- **Platform Admin:** `admin@staymart.com` / `Admin@123`
- **Student User:** `divyanshu@gehu.ac.in` / `Password@123`
"""
    with open(MD_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"[SUCCESS] Generated Markdown at: {MD_OUTPUT}")

if __name__ == '__main__':
    create_document()
    create_markdown()
