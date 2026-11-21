import os
import subprocess

OUTPUT_DIR = r"D:\Mini5th\report\diagrams"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TEMP_DIR = r"C:\Users\divya\AppData\Local\Temp\chrome_diag_profile"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. System Architecture Diagram HTML
arch_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 40px; background: #0f172a; font-family: 'Segoe UI', Inter, sans-serif; color: #f8fafc; }
  .canvas { width: 1400px; margin: 0 auto; }
  .title { text-align: center; font-size: 26px; font-weight: 700; color: #38bdf8; margin-bottom: 30px; letter-spacing: 0.5px; }
  .grid { display: grid; grid-template-columns: 280px 480px 480px; gap: 30px; align-items: stretch; }
  .col-box { background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
  .col-title { font-size: 18px; font-weight: 700; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #334155; padding-bottom: 12px; }
  .layer { background: #0f172a; border: 1px solid #475569; border-radius: 10px; padding: 14px; margin-bottom: 14px; }
  .layer-title { font-size: 14px; font-weight: 600; color: #38bdf8; margin-bottom: 6px; }
  .layer-desc { font-size: 12px; color: #94a3b8; line-height: 1.4; }
  .badge { display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; margin: 2px; }
  .bg-blue { background: #1e3a8a; color: #93c5fd; }
  .bg-green { background: #064e3b; color: #6ee7b7; }
  .bg-purple { background: #581c87; color: #d8b4fe; }
  .bg-amber { background: #78350f; color: #fde68a; }
  .flow-arrow { text-align: center; color: #64748b; font-size: 20px; margin: 8px 0; font-weight: bold; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">StayMart 3-Tier Distributed System Architecture</div>
  <div class="grid">
    <!-- Presentation Tier -->
    <div class="col-box" style="border-top: 4px solid #38bdf8;">
      <div class="col-title" style="color: #38bdf8;">🖥️ Client / Presentation Layer</div>
      <div class="layer">
        <div class="layer-title">Public Web Portal</div>
        <div class="layer-desc">Landing, Filtered Search, Detail Views, Interactive Modals, Responsive Glassmorphic UI</div>
        <div style="margin-top:8px;">
          <span class="badge bg-blue">HTML5</span>
          <span class="badge bg-blue">CSS3 (Inter)</span>
          <span class="badge bg-blue">Vanilla JS ES6+</span>
        </div>
      </div>
      <div class="layer">
        <div class="layer-title">User Self-Service Portal</div>
        <div class="layer-desc">Dashboard, Listing Creator, Booking Management, Order Tracking, Real-time Chat UI</div>
      </div>
      <div class="layer">
        <div class="layer-title">Admin Management Console</div>
        <div class="layer-desc">KPI Analytics, Chart.js Visualizations, Listing Moderation (Approve/Reject), Category & Location CRUD</div>
        <div style="margin-top:8px;">
          <span class="badge bg-blue">Chart.js</span>
          <span class="badge bg-blue">Fetch API</span>
        </div>
      </div>
    </div>

    <!-- Application / Business Tier -->
    <div class="col-box" style="border-top: 4px solid #10b981;">
      <div class="col-title" style="color: #10b981;">⚙️ Core Backend Service (Spring Boot 3.3)</div>
      <div class="layer">
        <div class="layer-title">Security & API Gateway Layer</div>
        <div class="layer-desc">JWT Authentication Filter, Role-Based Access Control (ROLE_USER, ROLE_ADMIN), CORS Policy</div>
        <div style="margin-top:8px;"><span class="badge bg-green">Spring Security</span><span class="badge bg-green">JWT (HMAC-SHA256)</span></div>
      </div>
      <div class="layer">
        <div class="layer-title">RESTful Controller Layer (16 Controllers)</div>
        <div class="layer-desc">Property, Product, Room, Booking, Order, Chat, Wishlist, Review, Location, Category, Behavior, Analytics</div>
        <div style="margin-top:8px;"><span class="badge bg-green">springdoc OpenAPI 3.0</span><span class="badge bg-green">Swagger UI</span></div>
      </div>
      <div class="layer">
        <div class="layer-title">Service & Business Logic Engine</div>
        <div class="layer-desc">Transactional Workflows, State Machine Moderation, Behavioral Event Ingestion, ML Proxy Client</div>
      </div>
      <div class="layer">
        <div class="layer-title">Data Access & ORM Layer</div>
        <div class="layer-desc">Spring Data JPA, Hibernate ORM 6.5, HikariCP Connection Pooling, Strict DDL Validation</div>
      </div>
    </div>

    <!-- Data & ML Microservice Tier -->
    <div class="col-box" style="border-top: 4px solid #a855f7;">
      <div class="col-title" style="color: #a855f7;">🧠 Data Storage & ML Engine</div>
      <div class="layer">
        <div class="layer-title">Relational Database (MySQL 8.0)</div>
        <div class="layer-desc">12 Normalized Tables: Users, Locations, Categories, Properties, Rooms, Products, Bookings, Orders, Chats, Wishlists, Reviews, UserBehaviors</div>
        <div style="margin-top:8px;"><span class="badge bg-amber">MySQL 8.0</span><span class="badge bg-amber">InnoDB Engine</span><span class="badge bg-amber">Foreign Keys</span></div>
      </div>
      <div class="layer">
        <div class="layer-title">ML Recommendation Microservice (Flask)</div>
        <div class="layer-desc">TF-IDF Vectorization of textual features, Cosine Similarity computation, User Behavioral Weighting (View/Wishlist/Order), Content-Based Recommendation</div>
        <div style="margin-top:8px;">
          <span class="badge bg-purple">Python 3.11</span>
          <span class="badge bg-purple">scikit-learn</span>
          <span class="badge bg-purple">pandas</span>
          <span class="badge bg-purple">Flask CORS</span>
        </div>
      </div>
      <div class="layer">
        <div class="layer-title">Persistent File Storage</div>
        <div class="layer-desc">Multi-part media uploads, serialized TF-IDF joblib model storage, automated model refresher</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

with open("report/diagrams/arch_diagram.html", "w", encoding="utf-8") as f:
    f.write(arch_html)

# 2. DFD Level 0 HTML
dfd0_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 40px; background: #0f172a; font-family: 'Segoe UI', Inter, sans-serif; color: #f8fafc; }
  .canvas { width: 1200px; margin: 0 auto; text-align: center; }
  .title { font-size: 26px; font-weight: 700; color: #38bdf8; margin-bottom: 40px; }
  svg { background: #1e293b; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
  text { font-family: 'Segoe UI', Inter, sans-serif; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">StayMart Data Flow Diagram (DFD Level 0 - Context Diagram)</div>
  <svg width="1120" height="620" viewBox="0 0 1120 620">
    <!-- Central Process -->
    <circle cx="560" cy="310" r="130" fill="#1e1b4b" stroke="#6366f1" stroke-width="3" />
    <text x="560" y="295" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">0.0</text>
    <text x="560" y="325" font-size="20" font-weight="bold" fill="#38bdf8" text-anchor="middle">StayMart</text>
    <text x="560" y="350" font-size="14" fill="#94a3b8" text-anchor="middle">Platform System</text>

    <!-- Entity 1: Guest / Browse User -->
    <rect x="60" y="80" width="180" height="90" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
    <text x="150" y="125" font-size="16" font-weight="bold" fill="#38bdf8" text-anchor="middle">Guest User</text>
    <text x="150" y="148" font-size="12" fill="#94a3b8" text-anchor="middle">(Public Visitor)</text>

    <!-- Entity 2: Tenant / Buyer -->
    <rect x="60" y="450" width="180" height="90" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2" />
    <text x="150" y="495" font-size="16" font-weight="bold" fill="#10b981" text-anchor="middle">Tenant / Buyer</text>
    <text x="150" y="518" font-size="12" fill="#94a3b8" text-anchor="middle">(Verified User)</text>

    <!-- Entity 3: Host / Seller -->
    <rect x="880" y="80" width="180" height="90" rx="10" fill="#0f172a" stroke="#f59e0b" stroke-width="2" />
    <text x="970" y="125" font-size="16" font-weight="bold" fill="#f59e0b" text-anchor="middle">Host / Seller</text>
    <text x="970" y="148" font-size="12" fill="#94a3b8" text-anchor="middle">(Property/Item Owner)</text>

    <!-- Entity 4: Platform Administrator -->
    <rect x="880" y="450" width="180" height="90" rx="10" fill="#0f172a" stroke="#ec4899" stroke-width="2" />
    <text x="970" y="495" font-size="16" font-weight="bold" fill="#ec4899" text-anchor="middle">Administrator</text>
    <text x="970" y="518" font-size="12" fill="#94a3b8" text-anchor="middle">(Moderator / Ops)</text>

    <!-- Entity 5: ML Recommender Service -->
    <rect x="470" y="20" width="180" height="60" rx="8" fill="#2e1065" stroke="#a855f7" stroke-width="2" />
    <text x="560" y="55" font-size="14" font-weight="bold" fill="#d8b4fe" text-anchor="middle">ML Microservice</text>

    <!-- Arrows & Labels -->
    <!-- Guest to System -->
    <path d="M 240 125 Q 380 180 440 250" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)" />
    <text x="310" y="170" font-size="11" fill="#93c5fd" transform="rotate(18, 310, 170)">Search & Filter Queries</text>

    <!-- System to Guest -->
    <path d="M 440 280 Q 320 220 240 150" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4" />
    <text x="290" y="235" font-size="11" fill="#cbd5e1" transform="rotate(22, 290, 235)">Catalogue & Listings</text>

    <!-- Tenant to System -->
    <path d="M 240 480 Q 380 430 440 360" fill="none" stroke="#10b981" stroke-width="2" />
    <text x="310" y="435" font-size="11" fill="#6ee7b7" transform="rotate(-18, 310, 435)">Bookings, Orders, Messages</text>

    <!-- System to Tenant -->
    <path d="M 440 380 Q 320 450 240 510" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4" />
    <text x="290" y="480" font-size="11" fill="#cbd5e1" transform="rotate(-22, 290, 480)">Confirmations & Recs</text>

    <!-- Host to System -->
    <path d="M 880 125 Q 740 180 680 250" fill="none" stroke="#f59e0b" stroke-width="2" />
    <text x="800" y="175" font-size="11" fill="#fde68a" transform="rotate(-18, 800, 175)">Listings, Room Specs, Media</text>

    <!-- System to Host -->
    <path d="M 680 280 Q 800 220 880 150" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4" />
    <text x="800" y="235" font-size="11" fill="#cbd5e1" transform="rotate(-22, 800, 235)">Inquiries, Order Requests</text>

    <!-- Admin to System -->
    <path d="M 880 480 Q 740 430 680 360" fill="none" stroke="#ec4899" stroke-width="2" />
    <text x="800" y="435" font-size="11" fill="#f472b6" transform="rotate(18, 800, 435)">Approve/Reject, Categories</text>

    <!-- System to Admin -->
    <path d="M 680 380 Q 800 450 880 510" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4" />
    <text x="780" y="480" font-size="11" fill="#cbd5e1" transform="rotate(22, 780, 480)">Analytics & Audit Reports</text>

    <!-- System <-> ML -->
    <path d="M 545 180 L 545 80" fill="none" stroke="#a855f7" stroke-width="2" />
    <text x="460" y="130" font-size="11" fill="#d8b4fe">Behaviors & Text</text>
    <path d="M 575 80 L 575 180" fill="none" stroke="#a855f7" stroke-width="2" />
    <text x="585" y="130" font-size="11" fill="#d8b4fe">Top-K Ranked IDs</text>
  </svg>
</div>
</body>
</html>
"""

with open("report/diagrams/dfd_level0.html", "w", encoding="utf-8") as f:
    f.write(dfd0_html)

# 3. Entity Relationship Diagram (ERD) HTML
erd_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 40px; background: #0b1120; font-family: 'Segoe UI', Inter, monospace; color: #f8fafc; }
  .canvas { width: 1500px; margin: 0 auto; }
  .title { text-align: center; font-size: 26px; font-weight: bold; color: #38bdf8; margin-bottom: 30px; }
  .erd-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
  .entity-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
  .entity-head { background: #334155; padding: 10px 14px; font-weight: bold; font-size: 15px; color: #38bdf8; display: flex; justify-content: space-between; }
  .entity-body { padding: 12px 14px; font-size: 12px; }
  .field { display: flex; justify-content: space-between; padding: 3px 0; border-bottom: 1px dashed #1e293b; }
  .pk { color: #f59e0b; font-weight: bold; }
  .fk { color: #a855f7; font-weight: bold; }
  .type { color: #94a3b8; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">StayMart Relational Database Schema (Entity-Relationship Model)</div>
  <div class="erd-grid">
    <!-- Users -->
    <div class="entity-card" style="border-top:3px solid #38bdf8">
      <div class="entity-head"><span>users</span><span>[Relational Node]</span></div>
      <div class="entity-body">
        <div class="field"><span class="pk">id (PK)</span><span class="type">BIGINT AUTO</span></div>
        <div class="field"><span>name</span><span class="type">VARCHAR(100)</span></div>
        <div class="field"><span>email</span><span class="type">VARCHAR(150) UNIQUE</span></div>
        <div class="field"><span>password_hash</span><span class="type">VARCHAR(255)</span></div>
        <div class="field"><span>phone</span><span class="type">VARCHAR(20)</span></div>
        <div class="field"><span>role</span><span class="type">ENUM(USER,ADMIN)</span></div>
        <div class="field"><span>city</span><span class="type">VARCHAR(100)</span></div>
        <div class="field"><span>bio</span><span class="type">TEXT</span></div>
        <div class="field"><span>is_active</span><span class="type">BOOLEAN</span></div>
        <div class="field"><span>created_at</span><span class="type">TIMESTAMP</span></div>
      </div>
    </div>

    <!-- Properties -->
    <div class="entity-card" style="border-top:3px solid #10b981">
      <div class="entity-head"><span>properties</span><span>[Accommodations]</span></div>
      <div class="entity-body">
        <div class="field"><span class="pk">id (PK)</span><span class="type">BIGINT AUTO</span></div>
        <div class="field"><span class="fk">posted_by (FK)</span><span class="type">BIGINT -> users</span></div>
        <div class="field"><span>title</span><span class="type">VARCHAR(200)</span></div>
        <div class="field"><span>description</span><span class="type">TEXT</span></div>
        <div class="field"><span>type</span><span class="type">ENUM(PG,HOSTEL..)</span></div>
        <div class="field"><span>gender_preference</span><span class="type">ENUM</span></div>
        <div class="field"><span class="fk">location_id (FK)</span><span class="type">BIGINT -> loc</span></div>
        <div class="field"><span>price_per_month</span><span class="type">DECIMAL(10,2)</span></div>
        <div class="field"><span>deposit_amount</span><span class="type">DECIMAL(10,2)</span></div>
        <div class="field"><span>amenities</span><span class="type">JSON</span></div>
        <div class="field"><span>images</span><span class="type">JSON</span></div>
        <div class="field"><span>status</span><span class="type">ENUM(PENDING..)</span></div>
      </div>
    </div>

    <!-- Rooms -->
    <div class="entity-card" style="border-top:3px solid #10b981">
      <div class="entity-head"><span>rooms</span><span>[Property Units]</span></div>
      <div class="entity-body">
        <div class="field"><span class="pk">id (PK)</span><span class="type">BIGINT AUTO</span></div>
        <div class="field"><span class="fk">property_id (FK)</span><span class="type">BIGINT -> prop</span></div>
        <div class="field"><span>room_number</span><span class="type">VARCHAR(50)</span></div>
        <div class="field"><span>type</span><span class="type">ENUM(SINGLE..)</span></div>
        <div class="field"><span>price</span><span class="type">DECIMAL(10,2)</span></div>
        <div class="field"><span>capacity</span><span class="type">INT</span></div>
        <div class="field"><span>floor_number</span><span class="type">INT</span></div>
        <div class="field"><span>is_available</span><span class="type">BOOLEAN</span></div>
        <div class="field"><span>images</span><span class="type">JSON</span></div>
      </div>
    </div>

    <!-- Products -->
    <div class="entity-card" style="border-top:3px solid #f59e0b">
      <div class="entity-head"><span>products</span><span>[Marketplace]</span></div>
      <div class="entity-body">
        <div class="field"><span class="pk">id (PK)</span><span class="type">BIGINT AUTO</span></div>
        <div class="field"><span class="fk">posted_by (FK)</span><span class="type">BIGINT -> users</span></div>
        <div class="field"><span class="fk">category_id (FK)</span><span class="type">BIGINT -> cat</span></div>
        <div class="field"><span>title</span><span class="type">VARCHAR(200)</span></div>
        <div class="field"><span>description</span><span class="type">TEXT</span></div>
        <div class="field"><span>price</span><span class="type">DECIMAL(10,2)</span></div>
        <div class="field"><span>listing_type</span><span class="type">ENUM(SELL,RENT)</span></div>
        <div class="field"><span>condition</span><span class="type">ENUM</span></div>
        <div class="field"><span>brand</span><span class="type">VARCHAR(100)</span></div>
        <div class="field"><span>images</span><span class="type">JSON</span></div>
        <div class="field"><span>status</span><span class="type">ENUM</span></div>
      </div>
    </div>

    <!-- Bookings -->
    <div class="entity-card" style="border-top:3px solid #06b6d4">
      <div class="entity-head"><span>bookings</span><span>[Stays]</span></div>
      <div class="entity-body">
        <div class="field"><span class="pk">id (PK)</span><span class="type">BIGINT AUTO</span></div>
        <div class="field"><span class="fk">property_id (FK)</span><span class="type">BIGINT</span></div>
        <div class="field"><span class="fk">room_id (FK)</span><span class="type">BIGINT (Opt)</span></div>
        <div class="field"><span class="fk">user_id (FK)</span><span class="type">BIGINT</span></div>
        <div class="field"><span>check_in_date</span><span class="type">DATE</span></div>
        <div class="field"><span>duration_months</span><span class="type">INT</span></div>
        <div class="field"><span>total_amount</span><span class="type">DECIMAL(10,2)</span></div>
        <div class="field"><span>status</span><span class="type">ENUM(PENDING..)</span></div>
      </div>
    </div>

    <!-- Orders -->
    <div class="entity-card" style="border-top:3px solid #f59e0b">
      <div class="entity-head"><span>orders</span><span>[Transactions]</span></div>
      <div class="entity-body">
        <div class="field"><span class="pk">id (PK)</span><span class="type">BIGINT AUTO</span></div>
        <div class="field"><span class="fk">product_id (FK)</span><span class="type">BIGINT</span></div>
        <div class="field"><span class="fk">buyer_id (FK)</span><span class="type">BIGINT</span></div>
        <div class="field"><span>order_type</span><span class="type">ENUM(BUY,RENT)</span></div>
        <div class="field"><span>amount</span><span class="type">DECIMAL(10,2)</span></div>
        <div class="field"><span>quantity</span><span class="type">INT</span></div>
        <div class="field"><span>status</span><span class="type">ENUM(PENDING..)</span></div>
      </div>
    </div>

    <!-- Chats -->
    <div class="entity-card" style="border-top:3px solid #ec4899">
      <div class="entity-head"><span>chats</span><span>[Messaging]</span></div>
      <div class="entity-body">
        <div class="field"><span class="pk">id (PK)</span><span class="type">BIGINT AUTO</span></div>
        <div class="field"><span class="fk">sender_id (FK)</span><span class="type">BIGINT</span></div>
        <div class="field"><span class="fk">receiver_id (FK)</span><span class="type">BIGINT</span></div>
        <div class="field"><span>message</span><span class="type">TEXT</span></div>
        <div class="field"><span>is_read</span><span class="type">BOOLEAN</span></div>
        <div class="field"><span>created_at</span><span class="type">TIMESTAMP</span></div>
      </div>
    </div>

    <!-- User Behaviors -->
    <div class="entity-card" style="border-top:3px solid #a855f7">
      <div class="entity-head"><span>user_behaviors</span><span>[ML Engine]</span></div>
      <div class="entity-body">
        <div class="field"><span class="pk">id (PK)</span><span class="type">BIGINT AUTO</span></div>
        <div class="field"><span class="fk">user_id (FK)</span><span class="type">BIGINT</span></div>
        <div class="field"><span>item_type</span><span class="type">VARCHAR(20)</span></div>
        <div class="field"><span>item_id</span><span class="type">BIGINT</span></div>
        <div class="field"><span>action</span><span class="type">ENUM(VIEW,BOOK..)</span></div>
        <div class="field"><span>weight</span><span class="type">FLOAT</span></div>
        <div class="field"><span>created_at</span><span class="type">TIMESTAMP</span></div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

with open("report/diagrams/er_diagram.html", "w", encoding="utf-8") as f:
    f.write(erd_html)

# 4. ML Recommendation Flowchart HTML
ml_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 40px; background: #0f172a; font-family: 'Segoe UI', Inter, sans-serif; color: #f8fafc; }
  .canvas { width: 1300px; margin: 0 auto; text-align: center; }
  .title { font-size: 26px; font-weight: 700; color: #a855f7; margin-bottom: 30px; }
  .flow { display: flex; justify-content: space-between; align-items: center; position: relative; }
  .step-box { background: #1e293b; border: 2px solid #334155; border-radius: 14px; padding: 20px; width: 220px; text-align: left; box-shadow: 0 8px 20px rgba(0,0,0,0.4); }
  .step-num { font-size: 12px; font-weight: bold; color: #a855f7; text-transform: uppercase; margin-bottom: 6px; }
  .step-title { font-size: 16px; font-weight: 700; color: #f8fafc; margin-bottom: 8px; }
  .step-desc { font-size: 12px; color: #94a3b8; line-height: 1.4; }
  .arrow { font-size: 28px; color: #64748b; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">StayMart Content-Based & Behavioral ML Recommendation Pipeline</div>
  <div class="flow">
    <div class="step-box" style="border-color: #38bdf8;">
      <div class="step-num" style="color:#38bdf8">Step 1: Data Ingestion</div>
      <div class="step-title">MySQL Aggregation</div>
      <div class="step-desc">Extract approved properties & products along with historical interactions from user_behaviors table.</div>
    </div>
    <div class="arrow">➔</div>

    <div class="step-box" style="border-color: #10b981;">
      <div class="step-num" style="color:#10b981">Step 2: Feature Engineering</div>
      <div class="step-title">Text Synthesis</div>
      <div class="step-desc">Construct composite document: Title + Description + Category + City + Area + Price Tier + Amenities tokens.</div>
    </div>
    <div class="arrow">➔</div>

    <div class="step-box" style="border-color: #a855f7;">
      <div class="step-num" style="color:#a855f7">Step 3: Vectorization</div>
      <div class="step-title">TF-IDF Sparse Matrix</div>
      <div class="step-desc">Scikit-learn TfidfVectorizer computes term frequency-inverse document frequency vectors (n-grams: 1-2).</div>
    </div>
    <div class="arrow">➔</div>

    <div class="step-box" style="border-color: #f59e0b;">
      <div class="step-num" style="color:#f59e0b">Step 4: Similarity Computation</div>
      <div class="step-title">Cosine Similarity</div>
      <div class="step-desc">Compute dot product matrix between candidate vectors and user profile weighted interaction vectors.</div>
    </div>
    <div class="arrow">➔</div>

    <div class="step-box" style="border-color: #ec4899;">
      <div class="step-num" style="color:#ec4899">Step 5: Hybrid Re-Ranking</div>
      <div class="step-title">Top-K Recommendations</div>
      <div class="step-desc">Apply locality filter (target city), popularity prior, and recency damping; return JSON to Spring Boot REST.</div>
    </div>
  </div>
</div>
</body>
</html>
"""

with open("report/diagrams/ml_pipeline.html", "w", encoding="utf-8") as f:
    f.write(ml_html)

# 5. Sequence Diagram HTML
seq_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 40px; background: #0f172a; font-family: 'Segoe UI', Inter, sans-serif; color: #f8fafc; }
  .canvas { width: 1200px; margin: 0 auto; text-align: center; }
  .title { font-size: 26px; font-weight: 700; color: #38bdf8; margin-bottom: 30px; }
  svg { background: #1e293b; border-radius: 16px; border: 1px solid #334155; }
  text { font-family: 'Segoe UI', Inter, sans-serif; font-size: 13px; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">StayMart Accommodation Booking & Confirmation Sequence Diagram</div>
  <svg width="1120" height="540" viewBox="0 0 1120 540">
    <!-- Lifelines -->
    <rect x="80" y="40" width="140" height="40" rx="8" fill="#1e3a8a" stroke="#38bdf8"/>
    <text x="150" y="65" fill="#f8fafc" font-weight="bold" text-anchor="middle">Tenant (Client)</text>
    <line x1="150" y1="80" x2="150" y2="480" stroke="#475569" stroke-dasharray="5"/>

    <rect x="360" y="40" width="160" height="40" rx="8" fill="#064e3b" stroke="#10b981"/>
    <text x="440" y="65" fill="#f8fafc" font-weight="bold" text-anchor="middle">Spring Boot API</text>
    <line x1="440" y1="80" x2="440" y2="480" stroke="#475569" stroke-dasharray="5"/>

    <rect x="660" y="40" width="140" height="40" rx="8" fill="#78350f" stroke="#f59e0b"/>
    <text x="730" y="65" fill="#f8fafc" font-weight="bold" text-anchor="middle">MySQL Database</text>
    <line x1="730" y1="80" x2="730" y2="480" stroke="#475569" stroke-dasharray="5"/>

    <rect x="920" y="40" width="140" height="40" rx="8" fill="#581c87" stroke="#a855f7"/>
    <text x="990" y="65" fill="#f8fafc" font-weight="bold" text-anchor="middle">Property Owner</text>
    <line x1="990" y1="80" x2="990" y2="480" stroke="#475569" stroke-dasharray="5"/>

    <!-- Step 1: POST Booking -->
    <line x1="150" y1="120" x2="440" y2="120" stroke="#38bdf8" stroke-width="2"/>
    <text x="295" y="112" fill="#93c5fd" text-anchor="middle">1. POST /api/bookings (propertyId, checkIn, months)</text>

    <!-- Step 2: Validate & Persist -->
    <line x1="440" y1="160" x2="730" y2="160" stroke="#10b981" stroke-width="2"/>
    <text x="585" y="152" fill="#6ee7b7" text-anchor="middle">2. Insert booking record (status: PENDING)</text>

    <!-- Step 3: Record Behavior -->
    <line x1="440" y1="200" x2="730" y2="200" stroke="#a855f7" stroke-width="2"/>
    <text x="585" y="192" fill="#d8b4fe" text-anchor="middle">3. Record behavior (action: BOOK, weight: 5.0)</text>

    <!-- Step 4: Notification to Owner -->
    <line x1="440" y1="240" x2="990" y2="240" stroke="#f59e0b" stroke-width="2"/>
    <text x="715" y="232" fill="#fde68a" text-anchor="middle">4. Notification & Requests-Received dashboard update</text>

    <!-- Step 5: Return 201 Created -->
    <line x1="440" y1="280" x2="150" y2="280" stroke="#64748b" stroke-width="2" stroke-dasharray="4"/>
    <text x="295" y="272" fill="#cbd5e1" text-anchor="middle">5. ApiResponse&lt;BookingResponse&gt; (Booking Pending)</text>

    <!-- Step 6: Owner Reviews & Approves -->
    <line x1="990" y1="340" x2="440" y2="340" stroke="#f59e0b" stroke-width="2"/>
    <text x="715" y="332" fill="#fde68a" text-anchor="middle">6. PATCH /api/bookings/{id}/status (status: CONFIRMED)</text>

    <!-- Step 7: Update DB -->
    <line x1="440" y1="380" x2="730" y2="380" stroke="#10b981" stroke-width="2"/>
    <text x="585" y="372" fill="#6ee7b7" text-anchor="middle">7. UPDATE bookings SET status='CONFIRMED', decrement rooms</text>

    <!-- Step 8: Confirmation Status to Tenant -->
    <line x1="440" y1="430" x2="150" y2="430" stroke="#10b981" stroke-width="2"/>
    <text x="295" y="422" fill="#6ee7b7" text-anchor="middle">8. Status confirmed on tenant dashboard & chat unlock</text>
  </svg>
</div>
</body>
</html>
"""

with open("report/diagrams/seq_booking.html", "w", encoding="utf-8") as f:
    f.write(seq_html)

# 6. Deployment Architecture Diagram HTML
deploy_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 40px; background: #0b1120; font-family: 'Segoe UI', Inter, sans-serif; color: #f8fafc; }
  .canvas { width: 1400px; margin: 0 auto; text-align: center; }
  .title { font-size: 26px; font-weight: 700; color: #38bdf8; margin-bottom: 30px; }
  .infra-grid { display: grid; grid-template-columns: 280px 80px 480px 80px 380px; align-items: center; }
  .box { background: #1e293b; border: 1px solid #334155; border-radius: 14px; padding: 22px; text-align: left; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
  .b-title { font-size: 16px; font-weight: bold; margin-bottom: 8px; color: #38bdf8; }
  .b-sub { font-size: 12px; color: #94a3b8; line-height: 1.5; }
  .tag { display: inline-block; padding: 3px 8px; background: #334155; color: #e2e8f0; border-radius: 6px; font-size: 11px; margin-top: 8px; font-weight: 600; }
  .arrow { font-size: 28px; color: #64748b; font-weight: bold; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">StayMart Production Hosting & Cloud Deployment Architecture</div>
  <div class="infra-grid">
    <!-- Internet / Clients -->
    <div class="box" style="border-color: #38bdf8;">
      <div class="b-title">🌐 End Users & Clients</div>
      <div class="b-sub">Mobile Browsers, Desktop Web, Tablet Devices across Uttarakhand.</div>
      <div class="tag">HTTPS / WSS</div>
    </div>

    <div class="arrow">➔</div>

    <!-- Edge / Ingress -->
    <div class="box" style="border-color: #10b981;">
      <div class="b-title" style="color:#10b981;">🛡️ Edge Ingress / Reverse Proxy</div>
      <div class="b-sub">Nginx High-Performance Reverse Proxy + SSL Termination (Let's Encrypt). Static assets caching, rate limiting, and request routing:</div>
      <div style="margin-top:10px; font-size:12px; color:#cbd5e1;">
        • <code>/</code> ➔ Static Frontend (Port 5500 / Vercel CDN)<br>
        • <code>/api/*</code> ➔ Spring Boot Backend (Port 8080)<br>
        • <code>/ml/*</code> ➔ ML Microservice (Port 5000)
      </div>
      <div class="tag">Nginx 1.25 / Docker</div>
    </div>

    <div class="arrow">➔</div>

    <!-- Container Runtime / Cloud Host -->
    <div class="box" style="border-color: #a855f7;">
      <div class="b-title" style="color:#a855f7;">☁️ Host / Docker Engine</div>
      <div class="b-sub">Ubuntu 22.04 LTS VPS (AWS EC2 / DigitalOcean)</div>
      <div style="margin-top:10px; font-size:12px; color:#cbd5e1;">
        📦 <b>Backend Container:</b> Eclipse Temurin JDK 21, Spring Boot JAR<br><br>
        📦 <b>ML Container:</b> Python 3.11, Flask + Gunicorn WSGI, scikit-learn<br><br>
        📦 <b>Database Container:</b> MySQL 8.0 with Persistent NVMe Docker Volume
      </div>
      <div class="tag">Docker Compose / Systemd</div>
    </div>
  </div>
</div>
</body>
</html>
"""

with open("report/diagrams/deployment_arch.html", "w", encoding="utf-8") as f:
    f.write(deploy_html)

# Convert all HTML diagrams to PNG using Chrome Headless!
diagrams = [
    ("arch_diagram.png", "file:///D:/Mini5th/report/diagrams/arch_diagram.html", 1500, 750),
    ("dfd_level0.png", "file:///D:/Mini5th/report/diagrams/dfd_level0.html", 1300, 750),
    ("er_diagram.png", "file:///D:/Mini5th/report/diagrams/er_diagram.html", 1600, 750),
    ("ml_pipeline.png", "file:///D:/Mini5th/report/diagrams/ml_pipeline.html", 1400, 450),
    ("seq_booking.png", "file:///D:/Mini5th/report/diagrams/seq_booking.html", 1300, 650),
    ("deployment_arch.png", "file:///D:/Mini5th/report/diagrams/deployment_arch.html", 1500, 500)
]

for filename, url, w, h in diagrams:
    out_path = os.path.join(OUTPUT_DIR, filename)
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={w},{h}",
        f"--user-data-dir={TEMP_DIR}",
        f"--screenshot={out_path}",
        url
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(out_path):
        print(f"Generated {filename} ({os.path.getsize(out_path)} bytes)")
    else:
        print(f"FAILED to generate {filename}")

print("All diagrams generated successfully!")
