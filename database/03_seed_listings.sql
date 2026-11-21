-- StayMart demo listings seed
-- Student accommodations (PG, hostel, flat, room, dormitory) and campus re-commerce classifieds across Uttarakhand.
-- Load AFTER database/01_schema.sql and database/02_seed.sql, before first app start.
-- All listings are inserted with status = APPROVED so they appear in the public catalogue.
--
-- Demo seller accounts: User@123
--   rohit.rawat@staymart.com / priya.negi@staymart.com / sunita.bisht@staymart.com / aman.chauhan@staymart.com
-- The admin account (admin@staymart.com / Admin@123) is created separately by DataSeeder.

USE staymart;

-- --------------------------------------------------------------------------
-- Demo users (hosts, students, passing-out seniors)
-- --------------------------------------------------------------------------
INSERT INTO users (id, name, email, password_hash, phone, role, city, state, bio, is_active, is_verified) VALUES
(2, 'Rohit Rawat',   'rohit.rawat@staymart.com',   '$2a$10$ECKbA6GnHPjFsppBN20t.eDs0xuDnnNX6trvH26lnhJEDqfbd.7Me', '9837001001', 'USER', 'Dehradun', 'Uttarakhand', 'B.Tech final-year senior & campus PG caretaker near Clement Town and Graphic Era.', TRUE, TRUE),
(3, 'Priya Negi',    'priya.negi@staymart.com',    '$2a$10$ECKbA6GnHPjFsppBN20t.eDs0xuDnnNX6trvH26lnhJEDqfbd.7Me', '9837001002', 'USER', 'Dehradun', 'Uttarakhand', 'Manages verified girls PGs and student flats in Rajpur Road and Subhash Nagar.', TRUE, TRUE),
(4, 'Sunita Bisht',  'sunita.bisht@staymart.com',  '$2a$10$ECKbA6GnHPjFsppBN20t.eDs0xuDnnNX6trvH26lnhJEDqfbd.7Me', '9837001003', 'USER', 'Dehradun', 'Uttarakhand', 'Runs student hostels and quiet study homestays across Dehradun and Mussoorie.', TRUE, TRUE),
(5, 'Aman Chauhan',  'aman.chauhan@staymart.com',  '$2a$10$ECKbA6GnHPjFsppBN20t.eDs0xuDnnNX6trvH26lnhJEDqfbd.7Me', '9837001004', 'USER', 'Dehradun', 'Uttarakhand', 'Graduating senior selling study equipment, electronics, and campus gear.', TRUE, TRUE);

-- --------------------------------------------------------------------------
-- Accommodations (12) : Student PGs, Hostels, Flats, Rooms, Dormitories
-- --------------------------------------------------------------------------
INSERT INTO properties
(id, posted_by, title, description, type, gender_preference, address, area, location_id, price_per_month, deposit_amount, amenities, total_rooms, available_rooms, images, status, is_available, created_at) VALUES
(1, 2, 'Sunrise Boys PG (Near Graphic Era University & ISBT)',
 'Well-maintained Boys PG within 800m of Graphic Era (GEU) & ISBT Dehradun. Includes 3 nutritious home-style meals (breakfast, lunch/tiffin, dinner), 100 Mbps WiFi, 24/7 power backup with inverter for exam weeks, attached washroom with geyser, daily cleaning, and zero brokerage.',
 'PG', 'MALE', 'Clement Town, Near Graphic Era University, Dehradun', 'Clement Town', 3, 6500.00, 6500.00,
 '["WiFi","AC","Hot Water","Laundry","Power Backup","Meals","Cleaning"]', 20, 8,
 '["https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 2 DAY)),

(2, 3, 'Green Valley Girls PG (Rajpur Road near DIT & Pacific Mall)',
 'Safe, secure Girls PG on Rajpur Road near Pacific Mall. Biometric entry, CCTV, and female warden. Fully furnished with individual box beds, study desks, ergonomic chairs, and almirahs. Fresh North & South Indian meals, RO water, and high-speed WiFi.',
 'PG', 'FEMALE', 'Rajpur Road, near Pacific Mall, Dehradun', 'Rajpur Road', 1, 8500.00, 17000.00,
 '["WiFi","AC","Hot Water","Security","Cleaning","Meals","Laundry"]', 15, 6,
 '["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 5 DAY)),

(3, 4, 'Comfort Student Hostel (Ballupur Chowk near FRI)',
 'Spacious and peaceful student hostel near Ballupur Chowk. Twin and triple sharing rooms with silent study hall and high-speed fiber internet. Wholesome mess meals with weekend specials, laundry facilities, and zero brokerage.',
 'HOSTEL', 'FEMALE', 'Ballupur Chowk, Dehradun', 'Ballupur', 6, 7000.00, 7000.00,
 '["WiFi","Hot Water","Power Backup","Security","Cleaning","Study Room","Meals"]', 30, 12,
 '["https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1540518614846-7ede433c4ef7?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 8 DAY)),

(4, 5, 'Tapovan Student & Nomad Bunk Dormitory (Rishikesh)',
 'Overlooking the hills of Tapovan, Rishikesh. Personal lockers, charging ports, 200 Mbps dual WiFi, rooftop coworking lounge with mountain views, and shared community kitchen. Ideal for remote study and travelers.',
 'DORMITORY', 'ANY', 'Tapovan, Rishikesh', 'Tapovan', 10, 4500.00, 4500.00,
 '["WiFi","Hot Water","Laundry","Lockers","Parking","Cleaning"]', 40, 18,
 '["https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 12 DAY)),

(5, 2, 'Independent Single Room for Students (Patel Nagar)',
 'Private entrance single room with attached bathroom in Patel Nagar. Includes single wooden cot, mattress, study desk, and geyser. Walking distance to libraries and coaching centers with zero interference.',
 'ROOM', 'MALE', 'Patel Nagar, Dehradun', 'Patel Nagar', 4, 4500.00, 4500.00,
 '["WiFi","Water","Power Backup"]', 8, 3,
 '["https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 1 DAY)),

(6, 3, 'Furnished 1BHK Student Flat (Subhash Nagar near GEHU)',
 'Ready-to-move furnished 1BHK flat in Subhash Nagar, 5 minutes scooty ride to Graphic Era Hill University. Double bed, study desks, modular kitchen with gas stove, and private balcony.',
 'FLAT', 'ANY', 'Subhash Nagar, Dehradun', 'Subhash Nagar', 8, 14000.00, 28000.00,
 '["WiFi","Parking","Furnished","Power Backup","Security"]', 1, 1,
 '["https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 3 DAY)),

(7, 4, 'Spacious 2BHK Flat for University Students (Sahastradhara Road)',
 'Sunny 2BHK flat ideal for 3-4 student roommates on Sahastradhara Road. Balconies facing Mussoorie hills, modular kitchen, 24/7 security guard, bike parking, and water backup.',
 'FLAT', 'ANY', 'Sahastradhara Road, Dehradun', 'Sahastradhara Road', 7, 18000.00, 36000.00,
 '["WiFi","Parking","Furnished","Power Backup","Water","Security"]', 1, 1,
 '["https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 6 DAY)),

(8, 5, 'Budget Guest Rooms & Student Long-Stay (Clock Tower Dehradun)',
 'Central rooms near Paltan Bazar and Railway Station. Ideal for outstation students during exam season and visiting parents. Includes study desk, high-speed WiFi, attached bath, and hot water.',
 'HOTEL', 'ANY', 'Clock Tower, Dehradun', 'Clock Tower', 2, 8000.00, 0.00,
 '["WiFi","AC","Hot Water","Cleaning","Meals","Parking"]', 25, 10,
 '["https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 9 DAY)),

(9, 2, 'Air-Cooled Dormitory Bed (Near Har Ki Pauri Ghat, Haridwar)',
 'Clean, economical dormitory bed within 300m of Har Ki Pauri ghats. Bunk beds with reading lamps, personal lockers, and RO drinking water. Convenient for entrance exam candidates.',
 'DORMITORY', 'ANY', 'Near Har Ki Pauri, Haridwar', 'Har Ki Pauri', 11, 3500.00, 3500.00,
 '["WiFi","Hot Water","Laundry","Lockers"]', 30, 14,
 '["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 15 DAY)),

(10, 3, 'Modern Co-living Studio (Kaonli Chowk / Balliwala)',
 'Contemporary co-living studio with kitchenette, induction cooktop, high-speed fiber WiFi, study table, and inverter backup. Peaceful environment ideal for final-year project work.',
 'ROOM', 'ANY', 'Kaonli Chowk, Dehradun', 'Kaonli', 5, 5500.00, 5500.00,
 '["WiFi","Furnished","AC","Cleaning","Power Backup"]', 6, 2,
 '["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1502005229762-ee1c8d067645?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 4 DAY)),

(11, 4, 'Pine Hill Student PG & Study Retreat (Mussoorie Mall Road)',
 'Quiet hill-facing student rooms with heaters and warm blankets, home-cooked Garhwali meals, and scenic valley views. Perfect for focused thesis writing and research study.',
 'PG', 'ANY', 'Mall Road, Mussoorie', 'Mall Road', 13, 7500.00, 7500.00,
 '["WiFi","Hot Water","Furnished","Meals","Cleaning"]', 12, 5,
 '["https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 20 DAY)),

(12, 5, 'Girls Student PG near IIT Roorkee Main Gate (Civil Lines)',
 'Located 600m from IIT Roorkee main gate in Civil Lines. Secure biometric entrance, 3 mess meals, high-speed internet, laundry area, and quiet study environment with zero brokerage.',
 'PG', 'FEMALE', 'Civil Lines, Roorkee', 'Civil Lines', 15, 6000.00, 6000.00,
 '["WiFi","AC","Hot Water","Security","Cleaning","Meals"]', 18, 7,
 '["https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 10 DAY));

-- --------------------------------------------------------------------------
-- Rooms for properties (single, double, triple, dormitory)
-- --------------------------------------------------------------------------
INSERT INTO rooms (property_id, room_number, type, price, capacity, floor_number, is_available, images) VALUES
(1, 'A-101', 'SINGLE', 6500.00, 1, 1, TRUE, '["https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=800&q=80"]'),
(1, 'A-102', 'DOUBLE', 5000.00, 2, 1, TRUE, '["https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80"]'),
(1, 'B-201', 'TRIPLE', 4200.00, 3, 2, FALSE, '["https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80"]'),
(2, 'G-01',  'SINGLE', 8500.00, 1, 0, TRUE, '["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80"]'),
(2, 'G-02',  'DOUBLE', 6500.00, 2, 0, TRUE, '["https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80"]'),
(3, 'H-101', 'DOUBLE', 7000.00, 2, 1, TRUE, '["https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80"]'),
(3, 'H-102', 'TRIPLE', 5500.00, 3, 1, TRUE, '["https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80"]'),
(3, 'D-01',  'DORMITORY', 4000.00, 6, 0, TRUE, '["https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=800&q=80"]');

-- --------------------------------------------------------------------------
-- Marketplace classifieds (24) : Student-to-student pre-loved campus essentials
-- --------------------------------------------------------------------------
INSERT INTO products
(id, posted_by, category_id, title, description, price, listing_type, `condition`, brand, location_id, area, images, status, is_available, views_count, created_at) VALUES
-- Electronics (category 7)
(1,  2, 7, 'Dell Inspiron 15 Laptop (11th Gen i5 / 16GB RAM / 512GB SSD)',
 'Used for 3 semesters of B.Tech CSE at GEHU. Boots in 6s, runs Android Studio & VS Code smoothly. Upgraded to 16GB dual-channel RAM. Includes original 65W charger, laptop sleeve, and bill.',
 32500.00, 'SELL', 'LIKE_NEW', 'Dell', 1, 'Rajpur Road',
 '["https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 210, DATE_SUB(NOW(), INTERVAL 1 DAY)),

(2,  3, 7, 'HP Pavilion Gaming 15 (Ryzen 5 5600H / GTX 1650 / 144Hz)',
 'Used for AutoCAD, SolidWorks projects, and casual gaming at UPES Bidholi. Fresh thermal paste applied last month. 144Hz display, 16GB RAM, 512GB SSD. Comes with 150W charger and cooling pad.',
 39500.00, 'SELL', 'GOOD', 'HP', 6, 'Ballupur',
 '["https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 165, DATE_SUB(NOW(), INTERVAL 3 DAY)),

(3,  4, 7, 'Apple MacBook Air M1 Space Grey (8GB RAM / 256GB SSD)',
 '92% battery health (gives 12-14 hours on-campus battery life). Selling because my placement company provided a work laptop. Pristine condition with original box, 30W charger, and protective skin.',
 56000.00, 'SELL', 'LIKE_NEW', 'Apple', 7, 'Sahastradhara Road',
 '["https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 320, DATE_SUB(NOW(), INTERVAL 2 DAY)),

(4,  5, 7, 'Canon EOS 1500D DSLR Kit + 18-55mm IS II Lens + 64GB Card',
 'Shutter count under 3,200. Used for college photography club and university cultural fests at Doon University. Includes 18-55mm lens, 2 original LP-E10 batteries, fast 64GB card, and padded camera bag.',
 21500.00, 'SELL', 'GOOD', 'Canon', 2, 'Clock Tower',
 '["https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 140, DATE_SUB(NOW(), INTERVAL 6 DAY)),

-- Mobile Phones (category 8)
(5,  2, 8, 'Apple iPhone 12 128GB Pacific Blue (Clean, 87% Battery)',
 'Always used with Spigen tempered glass and case. 87% battery health easily lasts a full day of college classes and hotspot. All cameras, True Tone, and Face ID work perfectly. Includes box and cable.',
 29500.00, 'SELL', 'GOOD', 'Apple', 1, 'Rajpur Road',
 '["https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 400, DATE_SUB(NOW(), INTERVAL 1 DAY)),

(6,  3, 8, 'Samsung Galaxy S21 5G 128GB (120Hz AMOLED / Phantom Grey)',
 'Used by DIT student for reading lecture PDFs and taking notes. 120Hz Dynamic AMOLED display, 30x space zoom for capturing whiteboard notes from back benches. Includes 25W fast charger and case.',
 24000.00, 'SELL', 'GOOD', 'Samsung', 3, 'ISBT',
 '["https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1580910051074-3eb694886505?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 260, DATE_SUB(NOW(), INTERVAL 4 DAY)),

(7,  4, 8, 'Redmi Note 12 Pro 5G 128GB (50MP Sony OIS / 67W Turbo Charger)',
 '7 months old, pristine condition. 67W charger does 0-100% in 45 minutes between classes. Sony IMX766 50MP camera with OIS. Includes original box, bill, and silicone cover.',
 13500.00, 'SELL', 'LIKE_NEW', 'Xiaomi', 5, 'Kaonli',
 '["https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 190, DATE_SUB(NOW(), INTERVAL 2 DAY)),

(8,  5, 8, 'OnePlus Nord CE 2 Lite 5G (8GB RAM / 128GB / 5000mAh)',
 'Snappy OxygenOS performance with 5000mAh battery that easily powers 1.5 days of hotspot. Dual 5G SIM support, 33W SuperVOOC charger, original red cable, and box included.',
 10500.00, 'SELL', 'LIKE_NEW', 'OnePlus', 8, 'Raipur Road',
 '["https://images.unsplash.com/photo-1567581935884-3349723552ca?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1511707171634-5f897ff02560?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 120, DATE_SUB(NOW(), INTERVAL 7 DAY)),

-- Furniture (category 9)
(9,  2, 9, 'Student Wooden Study Desk + Ergonomic Mesh Chair Combo',
 'Sturdy engineered wood study desk (3.5x2 ft) with drawer and cable grommet, paired with Green Soul breathable mid-back mesh chair. Perfect for long coding sprints and exam preparation. Senior moving out.',
 3200.00, 'SELL', 'GOOD', 'Green Soul', 1, 'Rajpur Road',
 '["https://images.unsplash.com/photo-1617806118233-18e1de247200?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 60, DATE_SUB(NOW(), INTERVAL 5 DAY)),

(10, 3, 9, 'Single Wooden Bed Cot (3x6 ft) + 5-Inch Foam Mattress',
 'Solid ply-board base single cot (3x6 ft) with Wakefit 5-inch orthopedic foam mattress and washable cover. Compact fit for any student PG room. Easily disassembles into 4 panels in 10 minutes.',
 3800.00, 'SELL', 'GOOD', 'Wakefit', 7, 'Sahastradhara Road',
 '["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1540518614846-7ede433c4ef7?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 88, DATE_SUB(NOW(), INTERVAL 9 DAY)),

(11, 4, 9, 'Foldable Bed Study Table + XL Leatherette Bean Bag Combo',
 'Compact foldable bed study table with tablet groove and cup holder, plus an XL brown leatherette bean bag filled with fresh beans. Great for late-night assignments and hostel room reading.',
 1400.00, 'SELL', 'GOOD', NULL, 4, 'Patel Nagar',
 '["https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 70, DATE_SUB(NOW(), INTERVAL 11 DAY)),

-- Books & Stationery (category 10)
(12, 5, 10, 'Class 11 & 12 JEE / Engineering Physics & Chemistry Bundle',
 'HC Verma Concepts of Physics Vol 1 & 2 + complete NCERT Physics and Chemistry textbooks. DC Pandey Mechanics included as free bonus. Clean pages with minimal pencil markings. Passed 1st year at Graphic Era.',
 950.00, 'SELL', 'GOOD', NULL, 4, 'Patel Nagar',
 '["https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1532012164546-f432f2e3777f?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 55, DATE_SUB(NOW(), INTERVAL 4 DAY)),

(13, 2, 10, 'GATE CSE & IT Complete Notes (Made Easy) + 15 Years Solved Papers',
 'Handwritten Made Easy classroom notes covering all 10 core CSE subjects (OS, DBMS, CN, TOC, Compiler, Algorithms, COA, Digital, Maths, Aptitude) plus 15 years chapter-wise solved papers.',
 1600.00, 'SELL', 'GOOD', 'Made Easy', 3, 'ISBT',
 '["https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 130, DATE_SUB(NOW(), INTERVAL 13 DAY)),

-- Home Appliances (category 11)
(14, 3, 11, 'Symphony Diet 35T Personal Tower Air Cooler with Stand & Trolley',
 '35-litre compact tower cooler with honeycomb pads and 4-wheel castor trolley. Low power consumption (170W) runs smoothly on student PG inverters during Dehradun summer heat. Senior passing out.',
 2400.00, 'SELL', 'GOOD', 'Symphony', 5, 'Kaonli',
 '["https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 95, DATE_SUB(NOW(), INTERVAL 6 DAY)),

(15, 4, 11, 'Whirlpool 190L Single Door Refrigerator (Direct Cool, 4-Star)',
 'Kept in a 2-student shared flat near Clement Town. Excellent cooling for summer drinks, water, and milk. 4-star energy rating adds barely ₹200 to monthly electricity bill. Clean and odor-free.',
 6500.00, 'SELL', 'GOOD', 'Whirlpool', 1, 'Rajpur Road',
 '["https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 110, DATE_SUB(NOW(), INTERVAL 8 DAY)),

(16, 5, 11, 'Winter Room Essentials: Bajaj 2000W Radiant Heater + Electric Kettle',
 'Bajaj 2000W halogen radiant room heater heats small rooms within 10 minutes for chilly Dehradun winters, paired with a Prestige 1.5L cordless electric kettle for midnight Maggi, coffee, and tea.',
 1100.00, 'SELL', 'GOOD', 'Bajaj', 7, 'Sahastradhara Road',
 '["https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 150, DATE_SUB(NOW(), INTERVAL 14 DAY)),

(17, 2, 11, 'Prestige 1600W Induction Cooktop + Non-Stick Frying Pan & Pot',
 'Allowed in student PGs where LPG cylinders are restricted. Push-button Indian menu presets (milk, boil, fry, chapati). Includes non-stick frying pan and stainless steel boiling pot with glass lid.',
 1500.00, 'SELL', 'GOOD', 'Prestige', 6, 'Ballupur',
 '["https://images.unsplash.com/photo-1570222094114-d054a817e56b?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 40, DATE_SUB(NOW(), INTERVAL 3 DAY)),

-- Vehicles (category 12)
(18, 3, 12, 'Honda Activa 6G (2021, UK-07 Passing) - Senior Moving Out',
 'Single owner, 9,450 km genuine reading, serviced regularly at authorized Honda service center. 50-52 kmpl mileage in Dehradun traffic. UK-07 RC, insurance valid till Nov 2026. B.Tech senior passing out.',
 52000.00, 'SELL', 'GOOD', 'Honda', 3, 'ISBT',
 '["https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 300, DATE_SUB(NOW(), INTERVAL 2 DAY)),

(19, 4, 12, 'Royal Enfield Classic 350 Stealth Black (2019 Dual ABS)',
 'Weekend cruiser used for Mussoorie, Dhanaulti, and Rishikesh trips. 14,200 km, pristine dual-channel ABS, Exide battery with 3-year warranty, crash guard with rope, and fog lights installed.',
 95000.00, 'SELL', 'GOOD', 'Royal Enfield', 2, 'Clock Tower',
 '["https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1558981359-219d6364c9c8?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 480, DATE_SUB(NOW(), INTERVAL 5 DAY)),

(20, 5, 12, 'Hero Sprint Pro 21-Speed Geared Mountain Bicycle with Number Lock',
 '21-speed Shimano derailleur and shifters, front telescopic suspension, and dual disc brakes. Saves daily auto fare between Clement Town and Graphic Era campus. Includes sturdy combination cable lock.',
 4500.00, 'SELL', 'GOOD', 'Hero', 4, 'Patel Nagar',
 '["https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1609630875171-b1321377ee65?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 220, DATE_SUB(NOW(), INTERVAL 10 DAY)),

-- Sports & Study Essentials (category 13)
(21, 2, 13, 'Yonex Nanoray 18i Carbon Graphite Racket + Shuttles Tube',
 '77g ultra-lightweight carbon graphite badminton racket strung at 24 lbs with BG-65 string. Includes full padded zip cover, fresh overgrip, and half-tube of Yonex Mavis 350 nylon shuttlecocks.',
 2200.00, 'RENT', 'GOOD', 'Yonex', 6, 'Ballupur',
 '["https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1613918108466-292b78a8ef95?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 65, DATE_SUB(NOW(), INTERVAL 4 DAY)),

(22, 3, 13, 'First-Year Engineering Drawing (ED) Complete Kit + White Lab Apron',
 'Essential first-year kit: Omega mini-drafter with carry pouch, imperial drawing board, sheet container tube, set squares, roller scale, French curves, and size 38 white cotton chemistry lab coat.',
 1200.00, 'SELL', 'GOOD', 'Omega', 5, 'Kaonli',
 '["https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 80, DATE_SUB(NOW(), INTERVAL 12 DAY)),

-- Fashion (category 15)
(23, 4, 15, 'Levis Original Trucker Denim Jacket (Size L) - Dark Indigo Blue',
 '100% heavy cotton denim trucker jacket, bought from Pacific Mall Dehradun. Worn only 2-3 times during college cultural fest and winter bonfire. Size L, authentic branded buttons and stitching.',
 1400.00, 'SELL', 'GOOD', 'Levis', 1, 'Rajpur Road',
 '["https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 44, DATE_SUB(NOW(), INTERVAL 3 DAY)),

-- Storage & Room Essentials (category 16)
(24, 5, 16, 'Collapsible 4-Tier Portable Clothes Wardrobe with Dust Cover',
 'Powder-coated steel pipe frame with zipped dustproof fabric cover and 4 tier fabric shelves. Assembles in 10 minutes without tools. Holds 25+ shirts and jackets. Folds flat to carry on a scooty.',
 950.00, 'SELL', 'GOOD', NULL, 5, 'Kaonli',
 '["https://images.unsplash.com/photo-1595428774223-ef52624120d2?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1558997519-83ea9252def8?auto=format&fit=crop&w=800&q=80"]', 'APPROVED', TRUE, 85, DATE_SUB(NOW(), INTERVAL 7 DAY));
