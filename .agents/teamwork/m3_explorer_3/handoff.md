# StayMart Technical Exploration Report & Humanization Blueprint

**Document:** `handoff.md`  
**Author:** Milestone 3 Explorer 3 (Frontend Copy, Seed Listings & Docs, Generation 2)  
**Parent Conversation ID:** `e8442687-110f-4189-bec3-f0fa5c033ec1`  
**Date:** November 2026  
**Target:** Milestone 3 (Content Humanization & AI Artifact Removal — UI Copy, Seed Listings & Documentation)

---

## 1. Observation

A direct code-level investigation of the frontend user interface copy, database fixtures, and repository documentation revealed specific large-language model (LLM) signatures, synthetic e-commerce placeholders, and corporate boilerplate.

### 1.1 `frontend/index.html`
- **Line 114–116**:
  ```html
  <p class="hero-subheadline">
    Zero Brokerage. Verified campus accommodations, pre-loved laptops, smartphones, two-wheelers and study furniture direct from university students and verified local owners.
  </p>
  ```
  *Finding*: Reads as generic e-commerce copy with no local campus resonance (lacks explicit university landmarks).
- **Line 507–510**:
  ```html
  <div class="step-card">
    <span class="step-icon">🤖</span>
    <h3>Smart ML Recommendations</h3>
    <p>Our TF-IDF AI algorithm matches your budget, campus proximity, and preferred amenities seamlessly.</p>
  </div>
  ```
  *Finding*: Blatant robotic AI phrasing exposing internal algorithm mechanics ("Our TF-IDF AI algorithm matches...") and LLM buzzwords ("seamlessly", robot emoji `🤖`).
- **Line 529–531**:
  ```html
  <p class="footer-desc" style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
    StayMart is Uttarakhand's premier community marketplace for verified student accommodations and pre-loved re-commerce across Dehradun, Rishikesh, Mussoorie and Roorkee.
  </p>
  ```
  *Finding*: Corporate hyperbole ("premier community marketplace").
- **Line 564–565**:
  ```html
  <div>© 2026 StayMart Marketplace Inc. · Built for Uttarakhand University Hubs</div>
  <div>💚 Zero Brokerage · 100% Student-to-Student</div>
  ```
  *Finding*: Corporate entity filler ("StayMart Marketplace Inc.").

### 1.2 `frontend/property-detail.html` & `frontend/product-detail.html`
- **`property-detail.html` Line 89–91 & 114**:
  ```html
  <p style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
    StayMart is Uttarakhand's premier student rental marketplace for verified PGs, hostels and shared flats near major campuses.
  </p>
  ...
  <div class="footer-bottom" style="margin-top:32px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.5);font-size:13px;">
    © 2026 StayMart Marketplace · Zero Brokerage Campus Living
  </div>
  ```
- **`product-detail.html` Line 88–90 & 113**:
  ```html
  <p style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
    StayMart is Uttarakhand's premier student classifieds platform for verified rentals and pre-loved gear.
  </p>
  ...
  <div class="footer-bottom" style="margin-top:32px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.5);font-size:13px;">
    © 2026 StayMart Marketplace · Made with 💚 for Dehradun Campuses
  </div>
  ```
- **`search-properties.html` Line 197 & `search-products.html` Line 191**:
  Both repeat variants of "Uttarakhand's premier rental and re-commerce marketplace".

### 1.3 `database/03_seed_listings.sql` & `database/05_olx_amazon_listings.sql`
- **`03_seed_listings.sql`**:
  Contains terse, robotic placeholder descriptions:
  - Property 1 (Line 27): `'Freshly painted boys PG 5 minutes walk from ISBT. Includes 3 meals, daily cleaning and 24x7 power backup. Ideal for students and working professionals.'`
  - Product 1 (Line 118): `'Barely used Dell Inspiron 15, core i5 11th gen, 8GB RAM and 512GB SSD. Under warranty till 2026, with original charger and box.'`
  - Product 9 (Line 159–161): `'Sheesham Wood 6-Seater Dining Table', 'Solid sheesham wood dining table with 6 cushioned chairs. Sturdy and polished, shifting sale hence priced to sell.'` (Suburban family furniture, not student hostel gear).
  - Product 10 (Line 164–165): `'Double Bed with Storage (Queen)'` (Price ₹12,000, hydraulic queen bed).
  - Product 11 (Line 169–171): `'3-Seater Fabric Sofa (Grey)'` (Price ₹15,500).
  - Product 16 (Line 196–198): `'Havells 1.5 Ton Split AC (3 Star)'` (Price ₹16,000).
  - Product 24 (Line 240–242): `'Godrej 2-Door Steel Almirah', '... Buyer to arrange transport.'` (Price ₹6,000).
- **`05_olx_amazon_listings.sql`**:
  While it enriched several electronics listings, Products 9, 10, 11, 16, and 24 still feature high-end suburban household goods instead of essential student equipment:
  - Passing-out seniors selling room coolers, geared bicycles, semester books, engineering drafters / lab coats, and single room study setups.
- **Generator Script**: `scripts/apply_olx_amazon_data.py` contains a duplicated Python multiline string used to overwrite `05_olx_amazon_listings.sql`.

### 1.4 `README.md`
- **Line 56**:
  `global.css # Shared theme (dark, indigo + mint)`
  *Finding*: Factual mismatch. `global.css` was updated to an authentic OLX / Amazon light theme (`--header-bg: #002f34`, `--bg-page: #f2f4f5`).
- **Line 111 & 121**: Mentions "Temurin JDK 21" when `pom.xml` targets `<java.version>17</java.version>`.
- **Line 273–275**:
  `## 🤖 Recommendation Engine`
  `The Flask service builds a TF-IDF recommender with scikit-learn:`
  *Finding*: Robotic phrasing and robot emoji header.

---

## 2. Logic Chain

1. **Premise 1 (Persona & Audience)**: StayMart is an open student platform created by and for university students living around Uttarakhand education corridors (Graphic Era, UPES Bidholi/Kandoli, DIT, Doon University, IIT Roorkee).
2. **Premise 2 (Zero AI Hallucination / Jargon)**: Students and evaluators assessing web applications immediately spot robotic AI jargon ("Our TF-IDF AI algorithm matches...", "seamlessly", "premier community marketplace", "Marketplace Inc.").
3. **Inference 1 (Frontend Copy Replacement)**: Replacing internal algorithm disclosures with user-centered value propositions ("Personalized Recommendations based on your campus and budget") makes the UI feel human-authored and trustworthy.
4. **Inference 2 (Footer Harmonization)**: Removing "Marketplace Inc." and "premier" across all five core pages (`index.html`, `property-detail.html`, `product-detail.html`, `search-properties.html`, `search-products.html`) ensures consistent, non-corporate student community branding: `© 2026 StayMart · Built for students in Uttarakhand`.
5. **Premise 3 (Hyperlocal Re-Commerce Realism)**: In real college clusters like Clement Town, Premnagar, Subhash Nagar, and Roorkee, passing-out final year students do not sell 6-seater Sheesham dining tables or 1.5-ton split ACs. They sell:
   - Personal room coolers (Symphony tower cooler with trolley stand for Dehradun summers).
   - Commuter bicycles (Hero Sprint 21-speed mountain bike with combination lock for campus travel).
   - Hostel study desks & ergonomic mesh chairs (for long coding sprints and GATE preparation).
   - Single wooden cots with foam mattresses and collapsible portable fabric wardrobes.
   - 1st Year Engineering Drawing (ED) kits (mini-drafter, sheet tube, drawing board) and white lab aprons.
   - Induction hotplates and electric kettles for hostel room snacks and midnight chai.
6. **Inference 3 (Database Seed Alignment)**: Transforming the sample listings in BOTH `03_seed_listings.sql` and `05_olx_amazon_listings.sql` (and its generator `scripts/apply_olx_amazon_data.py`) replaces synthetic e-commerce noise with authentic, localized student classifieds.
7. **Inference 4 (Documentation Truthfulness)**: Correcting `README.md` to reflect the actual OLX/Amazon light theme, Java 17 LTS, and conversational architecture descriptions eliminates AI artifacts from developer documentation.

---

## 3. Caveats

1. **LaTeX University Report Scope**: LaTeX chapters (`report/chapters/ch1_introduction.tex` to `ch9_conclusion.tex`) and report compilation (`scripts/compile_report_pdf.py`) are assigned to Milestone 3 Explorers 1 and 2. Explorer 3's scope is strictly frontend UI copy, SQL seed listings, and repository markdown documentation.
2. **Database Primary Keys & Schema Foreign Keys**: When updating descriptions in `03_seed_listings.sql` and `05_olx_amazon_listings.sql`, IDs (Properties 1–12, Products 1–24), category foreign keys (7 for Electronics, 8 for Mobile, 9 for Furniture, 10 for Books, 11 for Appliances, 12 for Vehicles, 13 for Sports, 15 for Fashion, 16 for Others), and location foreign keys (1 to 15) must remain stable so dependent tests and mock scripts do not break.
3. **Image URLs**: All image URLs in `database/04_update_realistic_media.sql` are matched by property/product ID and remain visually aligned with the humanized listings.

---

## 4. Conclusion & Implementation Blueprint

### File 1: `frontend/index.html`

#### Edit 1.1: Hero Sub-headline (Lines 114–116)
- **Before:**
  ```html
            <p class="hero-subheadline">
              Zero Brokerage. Verified campus accommodations, pre-loved laptops, smartphones, two-wheelers and study furniture direct from university students and verified local owners.
            </p>
  ```
- **After:**
  ```html
            <p class="hero-subheadline">
              Zero brokerage. Find verified PGs, hostels, and shared flats near Graphic Era, UPES, and DIT, or buy second-hand laptops, cycle commuters, books, and study gear directly from fellow students.
            </p>
  ```

#### Edit 1.2: Recommendation Value Proposition Card (Lines 506–510)
- **Before:**
  ```html
          <div class="step-card">
            <span class="step-icon">🤖</span>
            <h3>Smart ML Recommendations</h3>
            <p>Our TF-IDF AI algorithm matches your budget, campus proximity, and preferred amenities seamlessly.</p>
          </div>
  ```
- **After:**
  ```html
          <div class="step-card">
            <span class="step-icon">🎯</span>
            <h3>Personalized Recommendations</h3>
            <p>Find listings tailored to your campus, budget, and daily essentials based on what other students in your area look for.</p>
          </div>
  ```

#### Edit 1.3: Footer Description & Corporate Entity (Lines 529–531 & 564–565)
- **Before:**
  ```html
            <p class="footer-desc" style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
              StayMart is Uttarakhand's premier community marketplace for verified student accommodations and pre-loved re-commerce across Dehradun, Rishikesh, Mussoorie and Roorkee.
            </p>
  ```
  ```html
          <div>© 2026 StayMart Marketplace Inc. · Built for Uttarakhand University Hubs</div>
          <div>💚 Zero Brokerage · 100% Student-to-Student</div>
  ```
- **After:**
  ```html
            <p class="footer-desc" style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
              StayMart is a student-run marketplace for verified PG rentals and second-hand campus essentials across Dehradun, Rishikesh, Mussoorie, and Roorkee.
            </p>
  ```
  ```html
          <div>© 2026 StayMart · Built for students in Uttarakhand</div>
          <div>💚 Zero Brokerage · Direct student-to-student</div>
  ```

---

### File 2: `frontend/property-detail.html`

#### Edit 2.1: Footer Description & Bottom Copyright (Lines 89–91 & 113–115)
- **Before:**
  ```html
            <p style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
              StayMart is Uttarakhand's premier student rental marketplace for verified PGs, hostels and shared flats near major campuses.
            </p>
  ...
        <div class="footer-bottom" style="margin-top:32px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.5);font-size:13px;">
          © 2026 StayMart Marketplace · Zero Brokerage Campus Living
        </div>
  ```
- **After:**
  ```html
            <p style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
              StayMart helps students find verified PGs, hostels, and shared flats near major Uttarakhand university campuses with zero brokerage.
            </p>
  ...
        <div class="footer-bottom" style="margin-top:32px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.5);font-size:13px;display:flex;justify-content:space-between;align-items:center;">
          <div>© 2026 StayMart · Built for students in Uttarakhand</div>
          <div>Zero Brokerage · Direct student-to-student</div>
        </div>
  ```

---

### File 3: `frontend/product-detail.html`

#### Edit 3.1: Footer Description & Bottom Copyright (Lines 88–90 & 112–114)
- **Before:**
  ```html
            <p style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
              StayMart is Uttarakhand's premier student classifieds platform for verified rentals and pre-loved gear.
            </p>
  ...
        <div class="footer-bottom" style="margin-top:32px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.5);font-size:13px;">
          © 2026 StayMart Marketplace · Made with 💚 for Dehradun Campuses
        </div>
  ```
- **After:**
  ```html
            <p style="margin-top:14px;color:rgba(255,255,255,0.7);font-size:14px;max-width:340px;line-height:1.6">
              StayMart connects students across Dehradun and Uttarakhand to buy and sell pre-loved campus essentials with zero brokerage.
            </p>
  ...
        <div class="footer-bottom" style="margin-top:32px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.5);font-size:13px;display:flex;justify-content:space-between;align-items:center;">
          <div>© 2026 StayMart · Built for students in Uttarakhand</div>
          <div>Zero Brokerage · Direct student-to-student</div>
        </div>
  ```

---

### File 4: Complementary Frontend Pages (`search-properties.html` & `search-products.html`)
- In `frontend/search-properties.html` (Line 197): Replace "Uttarakhand's premier rental and re-commerce marketplace..." with:
  `StayMart connects students and tenants directly with verified PG owners and shared flats across Dehradun and Uttarakhand with zero brokerage.`
- In `frontend/search-products.html` (Line 191): Replace with:
  `StayMart connects students across Uttarakhand to buy and sell pre-loved campus essentials with zero brokerage.`

---

### File 5 & 6: Database Fixtures (`database/03_seed_listings.sql` & `database/05_olx_amazon_listings.sql`)

The 12 Accommodations and 24 Products are mapped below to provide humanized campus classifieds:

#### 12 Accommodations Master Table:
| ID | Type | Gender | Area | Humanized Title | Authentic Campus Description Highlights |
|:--:|:----:|:------:|:----:|:----------------|:----------------------------------------|
| 1 | PG | MALE | Clement Town | Sunrise Boys PG (Near Graphic Era University & ISBT) | 800m to GEU. 3 home-style meals, 100 Mbps WiFi, 24/7 power backup for exams, geyser, daily cleaning, zero brokerage. |
| 2 | PG | FEMALE | Rajpur Road | Green Valley Girls PG (Rajpur Road near DIT & Pacific Mall) | Safe locality, female warden, biometric entry, individual box beds, study desks, North & South Indian meals. |
| 3 | HOSTEL | FEMALE | Ballupur | Comfort Student Hostel (Ballupur Chowk near FRI) | Quick auto commute to FRI and Dev Bhoomi. Silent study hall, high-speed fiber internet, mess with weekend specials. |
| 4 | DORMITORY | ANY | Tapovan | Tapovan Student & Nomad Bunk Dormitory (Rishikesh) | Overlooking Tapovan hills. Personal lockers, charging ports, 200 Mbps dual WiFi, rooftop coworking lounge. |
| 5 | ROOM | MALE | Patel Nagar | Independent Single Room for Students (Patel Nagar) | Private entrance, study desk, single wooden cot, geyser, walking distance to coaching and reading rooms. No interference. |
| 6 | FLAT | ANY | Subhash Nagar | Furnished 1BHK Student Flat (Subhash Nagar near GEHU) | 5 mins scooty ride to Graphic Era Hill University. Double bed, study desks, modular kitchen, gas cylinder, balcony. |
| 7 | FLAT | ANY | Sahastradhara Road | Spacious 2BHK Flat for University Students (Sahastradhara Road) | Sunny 2BHK for 3-4 roommates. Balconies facing Mussoorie hills, modular kitchen, 24/7 security guard, bike parking. |
| 8 | HOTEL | ANY | Clock Tower | Budget Guest Rooms & Student Long-Stay (Clock Tower Dehradun) | Central rooms near Paltan Bazar for outstation exam takers and visiting parents. Study desk, WiFi, hot water. |
| 9 | DORMITORY | ANY | Har Ki Pauri | Air-Cooled Dormitory Bed (Near Har Ki Pauri Ghat, Haridwar) | 300m to ghats. Bunk beds with reading lamp, metal lockers, hot water, economical stay for entrance test takers. |
| 10 | ROOM | ANY | Kaonli | Modern Co-living Studio (Kaonli Chowk / Balliwala) | Contemporary studio with kitchenette, induction plate, fiber WiFi, study table, power backup. Ideal for final years. |
| 11 | PG | ANY | Mall Road | Pine Hill Student PG & Study Retreat (Mussoorie Mall Road) | Quiet hill-facing rooms with heaters and warm blankets, home-cooked Garhwali meals. Ideal for research/thesis writing. |
| 12 | PG | FEMALE | Civil Lines | Girls Student PG near IIT Roorkee Main Gate (Civil Lines) | 600m to IIT Roorkee main gate. Biometric security, 3 mess meals, laundry, quiet study environment. |

#### 24 Re-Commerce Products Master Table (All Student-Centered):
| ID | Category | Price (₹) | Condition | Humanized Title | Student Context & Authentic Details |
|:--:|:---------|:---------:|:---------:|:----------------|:------------------------------------|
| 1 | Electronics (7) | 32,500 | LIKE_NEW | Dell Inspiron 15 Laptop (11th Gen i5 / 16GB RAM / 512GB SSD) | Used for 3 semesters of B.Tech CSE at GEHU. Boots in 6s, runs Android Studio & VS Code. 65W charger + sleeve. |
| 2 | Electronics (7) | 39,500 | GOOD | HP Pavilion Gaming 15 (Ryzen 5 5600H / GTX 1650 / 144Hz) | Used for AutoCAD/SolidWorks & gaming at UPES Bidholi. Fresh thermal paste, 150W charger, cooling pad. |
| 3 | Electronics (7) | 56,000 | LIKE_NEW | Apple MacBook Air M1 Space Grey (8GB RAM / 256GB SSD) | 92% battery (12-14 hrs backup on campus). Placement company provided work laptop. Box and 30W charger. |
| 4 | Electronics (7) | 21,500 | GOOD | Canon EOS 1500D DSLR Kit + 18-55mm IS II Lens + 64GB Card | Shutter count <3,200. Used for Doon University photography club and fests. Bag, charger, 64GB card. |
| 5 | Mobile Phones (8) | 29,500 | GOOD | Apple iPhone 12 128GB Pacific Blue (Clean, 87% Battery) | Used with Spigen tempered glass. 87% battery lasts full college day. Box, cable, 2 spare covers. Upgrading post-placement. |
| 6 | Mobile Phones (8) | 24,000 | GOOD | Samsung Galaxy S21 5G 128GB (120Hz AMOLED / Phantom Grey) | DIT student used for reading lecture PDFs. 120Hz AMOLED, 30x zoom for whiteboard captures, Ringke case. |
| 7 | Mobile Phones (8) | 13,500 | LIKE_NEW | Redmi Note 12 Pro 5G 128GB (50MP Sony OIS / 67W Turbo Charger) | 7 months old, 67W charger does 0-100% in 45m between classes. Sony IMX766 camera, bill and box. |
| 8 | Mobile Phones (8) | 10,500 | LIKE_NEW | OnePlus Nord CE 2 Lite 5G (8GB RAM / 128GB / 5000mAh) | Snappy OxygenOS, 5000mAh battery lasts 1.5 days of hotspot. 33W charger, original red cable, box. |
| 9 | Furniture (9) | 3,200 | GOOD | Student Wooden Study Desk + Ergonomic Mesh Chair Combo | Replaces 6-seater dining table. Engineered wood desk (3.5x2 ft) + Green Soul mid-back mesh chair. 4th year senior moving out of Clement Town. |
| 10 | Furniture (9) | 3,800 | GOOD | Single Wooden Bed Cot (3x6 ft) + 5-Inch Foam Mattress | Replaces hydraulic double bed. Solid ply base cot (3x6 ft) + orthopedic foam mattress with washable cover. Disassembles in 10 mins. |
| 11 | Furniture (9) | 1,400 | GOOD | Foldable Bed Study Table + XL Leatherette Bean Bag Combo | Replaces 3-seater sofa. Bed desk with tablet groove + XL brown bean bag. Perfect for small PG rooms and late-night assignments. |
| 12 | Books (10) | 950 | GOOD | Class 11 & 12 JEE / Engineering Physics & Chemistry Bundle | HC Verma Vol 1 & 2 + NCERT Physics/Chemistry complete. DC Pandey Mechanics as free bonus. Passed 1st year at Graphic Era. |
| 13 | Books (10) | 1,600 | GOOD | GATE CSE & IT Complete Notes (Made Easy) + 15 Years Solved Papers | Made Easy classroom handwritten notes for all 10 core subjects + 15 years solved papers. Scored 65+ marks in GATE. |
| 14 | Appliances (11) | 2,400 | GOOD | Symphony Diet 35T Personal Tower Air Cooler with Stand & Trolley | Replaces semi-automatic washing machine. 35L tank, honeycomb pads, low power (runs on inverter). Senior passing out. |
| 15 | Appliances (11) | 6,500 | GOOD | Whirlpool 190L Single Door Refrigerator (Direct Cool, 4-Star) | Kept in 2-student flat in Clement Town for cold water and fruits. 4-star power savings (barely ₹200/mo). Spotless. |
| 16 | Appliances (11) | 1,100 | GOOD | Winter Room Essentials: Bajaj 2000W Radiant Heater + Electric Kettle | Replaces 1.5 ton AC. Halogen radiant heater heats room in 10m + Prestige 1.5L cordless kettle for midnight Maggi & tea. |
| 17 | Appliances (11) | 1,500 | GOOD | Prestige 1600W Induction Cooktop + Non-Stick Frying Pan & Pot | Allowed in all student PGs with no gas cylinder hassle. Indian menu presets, heats milk and makes eggs/maggi instantly. |
| 18 | Vehicles (12) | 52,000 | GOOD | Honda Activa 6G (2021, UK-07 Passing) - Senior Moving Out | 9,450 km genuine, 50-52 kmpl mileage in Dehradun traffic. UK-07 RC, insurance till Nov 2026. Passing out student. |
| 19 | Vehicles (12) | 95,000 | GOOD | Royal Enfield Classic 350 Stealth Black (2019 Dual ABS) | Weekend cruiser for Mussoorie & Rishikesh trips. Single owner, 14,200 km, Exide battery with 3-yr warranty, crash guard. |
| 20 | Vehicles (12) | 4,500 | GOOD | Hero Sprint Pro 21-Speed Geared Mountain Bicycle with Number Lock | Replaces Pulsar motorbike. 21-speed Shimano shifters, front suspension, disc brakes, combination cable lock. Saves auto fare. |
| 21 | Sports (13) | 2,200 | GOOD | Yonex Nanoray 18i Carbon Graphite Racket + Shuttles Tube | 77g ultra-lightweight carbon racket strung at 24 lbs. Padded cover, fresh grip, half tube Mavis 350 shuttles. |
| 22 | Study Gear (13/16) | 1,200 | GOOD | First-Year Engineering Drawing (ED) Complete Kit + White Lab Apron | Mini-drafter with carry pouch, wooden board, sheet tube, set squares, roller scale, French curves + white lab coat (size 38). |
| 23 | Fashion (15) | 1,400 | GOOD | Levis Original Trucker Denim Jacket (Size L) - Dark Indigo Blue | 100% heavy cotton denim, Pacific Mall purchase. Worn 2-3 times during college fest and winter bonfire. Size L. |
| 24 | Storage (16) | 950 | GOOD | Collapsible 4-Tier Portable Clothes Wardrobe with Dust Cover | Replaces Godrej steel almirah. Powder-coated steel frame, zipped dustproof fabric cover. Assembles in 10m, packs flat on scooty. |

---

### File 7: `README.md`

#### Edit 7.1: Project Summary (Lines 1–4)
- **Before:**
  ```markdown
  # StayMart 🏠

  StayMart is a full-stack accommodation and second-hand marketplace for **Dehradun and Uttarakhand**. Users can post and discover PGs, hostels, rooms, flats and hotels, buy or rent pre-loved products, book/view rooms, place orders, chat with owners and sellers, and leave reviews. Admins moderate listings, manage users, and view platform analytics. A Python ML microservice provides personalized and trending recommendations.
  ```
- **After:**
  ```markdown
  # StayMart 🏠

  StayMart is a student accommodation discovery and campus re-commerce web platform tailored for university hubs across Uttarakhand (Dehradun, Rishikesh, Haridwar, and Roorkee). The application connects students directly with verified PG owners and passing-out seniors with zero broker commission—allowing students to discover campus housing near Graphic Era, UPES, DIT, and IIT Roorkee, or buy essential second-hand gear including study desks, room coolers, bicycles, and textbooks.
  ```

#### Edit 7.2: Code Structure Description (Line 56)
- **Before:**
  ```markdown
  │   ├── css/
  │   │   ├── global.css          # Shared theme (dark, indigo + mint)
  │   │   └── dashboard.css       # Sidebar dashboard layouts
  ```
- **After:**
  ```markdown
  │   ├── css/
  │   │   ├── global.css          # Shared theme (OLX deep spruce + Amazon amber, mobile-first design)
  │   │   └── dashboard.css       # Sidebar dashboard layouts
  ```

#### Edit 7.3: Recommendation Engine Description (Lines 273–275)
- **Before:**
  ```markdown
  ## 🤖 Recommendation Engine

  The Flask service builds a TF-IDF recommender with scikit-learn:
  ```
- **After:**
  ```markdown
  ## 🎯 Recommendation Engine

  StayMart uses a dedicated Python Flask microservice to compute content-based recommendations using scikit-learn:
  ```

#### Edit 7.4: Demo Listings Summary (Lines 207–216)
- **Before:**
  ```markdown
  - **12 accommodations** (PG, hostel, flat, room, hotel, dormitory) across Dehradun, Rishikesh, Haridwar, Mussoorie and Roorkee — OYO / PG / hostel style, with amenities, monthly rent, deposits and images.
  - **8 rooms** attached to the first three PGs/hostels (shown on the property detail page).
  - **24 products** — OLX-style used goods (laptops, phones, furniture, books, appliances, bikes, sports gear, fashion) with price, condition, listing type, brand, location and images.
  ```
- **After:**
  ```markdown
  - **12 accommodations** (student PGs, girls/boys hostels, shared flats, and single rooms) across Dehradun, Rishikesh, Haridwar, Mussoorie and Roorkee with verified amenities, transparent student rent, meal inclusions, and zero brokerage.
  - **8 rooms** attached to the first three campus PGs/hostels (single, double, and triple sharing rooms with availability tracking).
  - **24 student classifieds** — authentic pre-loved campus essentials (coding laptops, room coolers, bicycles, study desk combos, GATE notes, engineering drawing kits, and induction cookware) posted by graduating seniors.
  ```

---

## 5. Verification Method

To verify these changes independently once implemented:

1. **Static UI Verification**:
   - Inspect `frontend/index.html` lines 110–120 and 500–515 to confirm:
     - No occurrence of `"TF-IDF AI algorithm"`.
     - No occurrence of `"Marketplace Inc."`.
     - Step 2 reads `"Personalized Recommendations"` with student-centric text.
   - Run a grep check across `frontend/`:
     ```powershell
     rg -i "TF-IDF|Marketplace Inc|premier community" frontend/
     ```
     *Expected result*: 0 matches.

2. **Database Seed Integrity Check**:
   - Verify that `database/03_seed_listings.sql` and `database/05_olx_amazon_listings.sql` contain the 24 student-tailored titles (coolers, bicycles, engineering drawing kits, study desk combos).
   - Verify SQL syntax:
     ```powershell
     Get-Content database/03_seed_listings.sql, database/05_olx_amazon_listings.sql | Out-Null
     ```
     Ensure valid string escaping (e.g. `''` for single quotes within descriptions).

3. **Backend Unit Tests**:
   - Run the existing backend test suite to ensure entity models and JPA mappings remain 100% green:
     ```powershell
     python scripts/run_backend_tests.py
     ```
     *Expected result*: Exit code 0, 13/13 tests passing.

4. **Responsive Layout Verification**:
   - Run the mobile viewport layout verification suite:
     ```powershell
     node scripts/run_viewport_tests.js
     ```
     *Expected result*: All pages render with 0 horizontal overflows across 375px, 768px, and 1280px viewports.
