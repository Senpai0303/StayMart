-- StayMart demo listings seed
-- Marketplace products (OLX-style) and accommodations (OYO / PG / hostel style) around Uttarakhand.
-- Load AFTER database/01_schema.sql and database/02_seed.sql, ideally before first app start.
-- All listings are inserted with status = APPROVED so they show up in the public catalogue.
--
-- Demo seller accounts (added by this script) all use the password:  User@123
--   rohit.rawat@staymart.com / priya.negi@staymart.com / sunita.bisht@staymart.com / aman.chauhan@staymart.com
-- The admin account (admin@staymart.com / Admin@123) is created separately by the app's DataSeeder.

USE staymart;

-- --------------------------------------------------------------------------
-- Demo sellers (sellers/owners of the listings below)
-- --------------------------------------------------------------------------
INSERT INTO users (id, name, email, password_hash, phone, role, city, state, bio, is_active, is_verified) VALUES
(2, 'Rohit Rawat',   'rohit.rawat@staymart.com',   '$2a$10$ECKbA6GnHPjFsppBN20t.eDs0xuDnnNX6trvH26lnhJEDqfbd.7Me', '9837001001', 'USER', 'Dehradun', 'Uttarakhand', 'Local host & used-goods seller around ISBT and Rajpur Road.', TRUE, TRUE),
(3, 'Priya Negi',    'priya.negi@staymart.com',    '$2a$10$ECKbA6GnHPjFsppBN20t.eDs0xuDnnNX6trvH26lnhJEDqfbd.7Me', '9837001002', 'USER', 'Dehradun', 'Uttarakhand', 'Manages girls PG and co-living spaces in Dehradun.', TRUE, TRUE),
(4, 'Sunita Bisht',  'sunita.bisht@staymart.com',  '$2a$10$ECKbA6GnHPjFsppBN20t.eDs0xuDnnNX6trvH26lnhJEDqfbd.7Me', '9837001003', 'USER', 'Dehradun', 'Uttarakhand', 'Runs hostels and homestays across the hills.', TRUE, TRUE),
(5, 'Aman Chauhan',  'aman.chauhan@staymart.com',  '$2a$10$ECKbA6GnHPjFsppBN20t.eDs0xuDnnNX6trvH26lnhJEDqfbd.7Me', '9837001004', 'USER', 'Dehradun', 'Uttarakhand', 'Sells electronics, vehicles and gadgets.', TRUE, TRUE);

-- --------------------------------------------------------------------------
-- Accommodations (12) : PG, hostel, flat, room, hotel, dormitory
-- --------------------------------------------------------------------------
INSERT INTO properties
(id, posted_by, title, description, type, gender_preference, address, area, location_id, price_per_month, deposit_amount, amenities, total_rooms, available_rooms, images, status, is_available, created_at) VALUES
(1, 2, 'Sunrise Boys PG near ISBT',
 'Freshly painted boys PG 5 minutes walk from ISBT. Includes 3 meals, daily cleaning and 24x7 power backup. Ideal for students and working professionals.',
 'PG', 'MALE', 'Near ISBT Bus Stand, Dehradun', 'ISBT', 3, 6500.00, 6500.00,
 '["WiFi","AC","Hot Water","Laundry","Power Backup","Meals","Cleaning"]', 20, 8,
 '["https://picsum.photos/seed/staymart-pg1a/800/600","https://picsum.photos/seed/staymart-pg1b/800/600","https://picsum.photos/seed/staymart-pg1c/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 2 DAY)),

(2, 3, 'Green Valley Girls PG, Rajpur Road',
 'Safe and fully furnished girls PG on Rajpur Road with warden, CCTV and biometric entry. Attached washrooms, RO water and home-style meals.',
 'PG', 'FEMALE', 'Rajpur Road, Dehradun', 'Rajpur Road', 1, 8500.00, 17000.00,
 '["WiFi","AC","Hot Water","Security","Cleaning","Meals","Laundry"]', 15, 6,
 '["https://picsum.photos/seed/staymart-pg2a/800/600","https://picsum.photos/seed/staymart-pg2b/800/600","https://picsum.photos/seed/staymart-pg2c/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 5 DAY)),

(3, 4, 'Comfort Girls Hostel, Ballupur',
 'Girls hostel with single and sharing rooms, study hall and mess. Walking distance from Ballupur Chowk and IT parks.',
 'HOSTEL', 'FEMALE', 'Ballupur Chowk, Dehradun', 'Ballupur', 6, 7000.00, 7000.00,
 '["WiFi","Hot Water","Power Backup","Security","Cleaning","Study Room","Meals"]', 30, 12,
 '["https://picsum.photos/seed/staymart-hostel1a/800/600","https://picsum.photos/seed/staymart-hostel1b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 8 DAY)),

(4, 5, 'Backpackers Dorm, Tapovan Rishikesh',
 'Budget backpacker dorm near Laxman Jhula with lockers, common lounge and rooftop cafe. Popular with travellers and yoga students.',
 'DORMITORY', 'ANY', 'Tapovan, Rishikesh', 'Tapovan', 10, 4500.00, 4500.00,
 '["WiFi","Hot Water","Laundry","Lockers","Parking","Cleaning"]', 40, 18,
 '["https://picsum.photos/seed/staymart-dorm1a/800/600","https://picsum.photos/seed/staymart-dorm1b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 12 DAY)),

(5, 2, 'Budget Single Room, Patel Nagar',
 'Independent single room with attached bathroom and kitchenette. Separate entry, suitable for working bachelors.',
 'ROOM', 'MALE', 'Patel Nagar, Dehradun', 'Patel Nagar', 4, 4500.00, 4500.00,
 '["WiFi","Water","Power Backup"]', 8, 3,
 '["https://picsum.photos/seed/staymart-room1a/800/600","https://picsum.photos/seed/staymart-room1b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 1 DAY)),

(6, 3, 'Furnished 1BHK Flat, Raipur Road',
 'Bright 1BHK flat fully furnished with bed, wardrobe, sofa and modular kitchen. Gated society with lift and covered parking.',
 'FLAT', 'ANY', 'Raipur Road, Dehradun', 'Raipur Road', 8, 14000.00, 28000.00,
 '["WiFi","Parking","Furnished","Power Backup","Security"]', 1, 1,
 '["https://picsum.photos/seed/staymart-flat1a/800/600","https://picsum.photos/seed/staymart-flat1b/800/600","https://picsum.photos/seed/staymart-flat1c/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 3 DAY)),

(7, 4, 'Spacious 2BHK Flat, Sahastradhara Road',
 'Semi-furnished 2BHK with balcony and scenic valley view. 24x7 water, gated parking and close to schools and market.',
 'FLAT', 'ANY', 'Sahastradhara Road, Dehradun', 'Sahastradhara Road', 7, 22000.00, 44000.00,
 '["WiFi","Parking","Furnished","Power Backup","Water","Security"]', 1, 1,
 '["https://picsum.photos/seed/staymart-flat2a/800/600","https://picsum.photos/seed/staymart-flat2b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 6 DAY)),

(8, 5, 'Hotel Silver Oak, Clock Tower',
 'Centrally located budget hotel offering monthly long-stay rates. Air-conditioned rooms, room service, laundry and in-house restaurant.',
 'HOTEL', 'ANY', 'Clock Tower, Dehradun', 'Clock Tower', 2, 15000.00, 0.00,
 '["WiFi","AC","Hot Water","Cleaning","Meals","Parking"]', 25, 10,
 '["https://picsum.photos/seed/staymart-hotel1a/800/600","https://picsum.photos/seed/staymart-hotel1b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 9 DAY)),

(9, 2, 'Ganga View Dorm Bed, Haridwar',
 'Clean dormitory beds 10 minutes from Har Ki Pauri. Hot water, lockers and a shared kitchen. Great for pilgrims and backpackers.',
 'DORMITORY', 'ANY', 'Near Har Ki Pauri, Haridwar', 'Har Ki Pauri', 11, 3500.00, 3500.00,
 '["WiFi","Hot Water","Laundry","Lockers"]', 30, 14,
 '["https://picsum.photos/seed/staymart-dorm2a/800/600","https://picsum.photos/seed/staymart-dorm2b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 15 DAY)),

(10, 3, 'Co-living Studio, Kaonli',
 'Modern co-living studio for professionals with high-speed WiFi, housekeeping and community kitchen. All bills included.',
 'ROOM', 'ANY', 'Kaonli, Dehradun', 'Kaonli', 5, 11000.00, 11000.00,
 '["WiFi","Furnished","AC","Cleaning","Power Backup"]', 6, 2,
 '["https://picsum.photos/seed/staymart-studio1a/800/600","https://picsum.photos/seed/staymart-studio1b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 4 DAY)),

(11, 4, 'Mountain View PG, Mussoorie Mall Road',
 'Cosy PG on Mall Road with mountain-facing rooms, heater, and home-cooked meals. Perfect for seasonal workers and students.',
 'PG', 'ANY', 'Mall Road, Mussoorie', 'Mall Road', 13, 9000.00, 9000.00,
 '["WiFi","Hot Water","Furnished","Meals","Cleaning"]', 12, 5,
 '["https://picsum.photos/seed/staymart-pg3a/800/600","https://picsum.photos/seed/staymart-pg3b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 20 DAY)),

(12, 5, 'Working Women PG, Roorkee Civil Lines',
 'Secure working women PG near Civil Lines with warden, CCTV, biometric entry, meals and laundry. Close to IIT Roorkee.',
 'PG', 'FEMALE', 'Civil Lines, Roorkee', 'Civil Lines', 15, 6000.00, 6000.00,
 '["WiFi","AC","Hot Water","Security","Cleaning","Meals"]', 18, 7,
 '["https://picsum.photos/seed/staymart-pg4a/800/600","https://picsum.photos/seed/staymart-pg4b/800/600"]', 'APPROVED', TRUE, DATE_SUB(NOW(), INTERVAL 10 DAY));

-- --------------------------------------------------------------------------
-- Rooms for a few accommodations (shown on the property detail page)
-- --------------------------------------------------------------------------
INSERT INTO rooms (property_id, room_number, type, price, capacity, floor_number, is_available, images) VALUES
(1, 'A-101', 'SINGLE', 6500.00, 1, 1, TRUE, '["https://picsum.photos/seed/staymart-room-a101/600/400"]'),
(1, 'A-102', 'DOUBLE', 5000.00, 2, 1, TRUE, '["https://picsum.photos/seed/staymart-room-a102/600/400"]'),
(1, 'B-201', 'TRIPLE', 4200.00, 3, 2, FALSE, '["https://picsum.photos/seed/staymart-room-b201/600/400"]'),
(2, 'G-01',  'SINGLE', 8500.00, 1, 0, TRUE, '["https://picsum.photos/seed/staymart-room-g01/600/400"]'),
(2, 'G-02',  'DOUBLE', 6500.00, 2, 0, TRUE, '["https://picsum.photos/seed/staymart-room-g02/600/400"]'),
(3, 'H-101', 'DOUBLE', 7000.00, 2, 1, TRUE, '["https://picsum.photos/seed/staymart-room-h101/600/400"]'),
(3, 'H-102', 'TRIPLE', 5500.00, 3, 1, TRUE, '["https://picsum.photos/seed/staymart-room-h102/600/400"]'),
(3, 'D-01',  'DORMITORY', 4000.00, 6, 0, TRUE, '["https://picsum.photos/seed/staymart-room-d01/600/400"]');

-- --------------------------------------------------------------------------
-- Marketplace products (24) : OLX-style used goods across Dehradun
-- --------------------------------------------------------------------------
INSERT INTO products
(id, posted_by, category_id, title, description, price, listing_type, `condition`, brand, location_id, area, images, status, is_available, views_count, created_at) VALUES
-- Electronics (category 7)
(1,  2, 7, 'Dell Inspiron 15 3000 (i5, 8GB/512GB)',
 'Barely used Dell Inspiron 15, core i5 11th gen, 8GB RAM and 512GB SSD. Under warranty till 2026, with original charger and box.',
 32000.00, 'SELL', 'LIKE_NEW', 'Dell', 1, 'Rajpur Road',
 '["https://picsum.photos/seed/staymart-dell1/800/600","https://picsum.photos/seed/staymart-dell2/800/600"]', 'APPROVED', TRUE, 210, DATE_SUB(NOW(), INTERVAL 1 DAY)),

(2,  3, 7, 'HP Pavilion Gaming Laptop (GTX 1650)',
 'HP Pavilion gaming laptop with Ryzen 5, 16GB RAM, 512GB SSD and GTX 1650 4GB graphics. Runs all popular games smoothly. Minor scratch on lid.',
 41000.00, 'SELL', 'GOOD', 'HP', 6, 'Ballupur',
 '["https://picsum.photos/seed/staymart-hp1/800/600","https://picsum.photos/seed/staymart-hp2/800/600"]', 'APPROVED', TRUE, 165, DATE_SUB(NOW(), INTERVAL 3 DAY)),

(3,  4, 7, 'Apple MacBook Air M1 (8GB/256GB)',
 'Apple MacBook Air M1 in excellent condition, battery health 92 percent. Ideal for students and developers. Comes with charger and sleeve.',
 62000.00, 'SELL', 'LIKE_NEW', 'Apple', 7, 'Sahastradhara Road',
 '["https://picsum.photos/seed/staymart-mac1/800/600","https://picsum.photos/seed/staymart-mac2/800/600"]', 'APPROVED', TRUE, 320, DATE_SUB(NOW(), INTERVAL 2 DAY)),

(4,  5, 7, 'Canon EOS 1500D DSLR + 18-55mm Lens',
 'Canon EOS 1500D with kit lens, 2 batteries, 32GB card and bag. Shutter count under 8000. Great for beginners and vloggers.',
 19500.00, 'SELL', 'GOOD', 'Canon', 2, 'Clock Tower',
 '["https://picsum.photos/seed/staymart-canon1/800/600","https://picsum.photos/seed/staymart-canon2/800/600"]', 'APPROVED', TRUE, 140, DATE_SUB(NOW(), INTERVAL 6 DAY)),

-- Mobile Phones (category 8)
(5,  2, 8, 'Apple iPhone 12 128GB',
 'iPhone 12 128GB in good condition, battery health 85 percent. Face ID working, no scratches. With box and original cable.',
 33000.00, 'SELL', 'GOOD', 'Apple', 1, 'Rajpur Road',
 '["https://picsum.photos/seed/staymart-iphone1/800/600","https://picsum.photos/seed/staymart-iphone2/800/600"]', 'APPROVED', TRUE, 400, DATE_SUB(NOW(), INTERVAL 1 DAY)),

(6,  3, 8, 'Samsung Galaxy S21 5G 128GB',
 'Samsung Galaxy S21 5G, phantom grey, 8GB RAM 128GB storage. Display flawless, includes 25W charger.',
 27500.00, 'SELL', 'GOOD', 'Samsung', 3, 'ISBT',
 '["https://picsum.photos/seed/staymart-s21a/800/600","https://picsum.photos/seed/staymart-s21b/800/600"]', 'APPROVED', TRUE, 260, DATE_SUB(NOW(), INTERVAL 4 DAY)),

(7,  4, 8, 'Redmi Note 12 Pro 5G',
 'Redmi Note 12 Pro 5G, 8GB/128GB, 3 months old. Under warranty, with box, charger and bill.',
 14500.00, 'SELL', 'LIKE_NEW', 'Xiaomi', 5, 'Kaonli',
 '["https://picsum.photos/seed/staymart-redmi1/800/600","https://picsum.photos/seed/staymart-redmi2/800/600"]', 'APPROVED', TRUE, 190, DATE_SUB(NOW(), INTERVAL 2 DAY)),

(8,  5, 8, 'OnePlus Nord CE 2 Lite 5G',
 'OnePlus Nord CE 2 Lite 5G, 6GB/128GB, used for 8 months. Smooth performance, 5000mAh battery. Charger included.',
 11000.00, 'SELL', 'LIKE_NEW', 'OnePlus', 8, 'Raipur Road',
 '["https://picsum.photos/seed/staymart-oneplus1/800/600","https://picsum.photos/seed/staymart-oneplus2/800/600"]', 'APPROVED', TRUE, 120, DATE_SUB(NOW(), INTERVAL 7 DAY)),

-- Furniture (category 9)
(9,  2, 9, 'Sheesham Wood 6-Seater Dining Table',
 'Solid sheesham wood dining table with 6 cushioned chairs. Sturdy and polished, shifting sale hence priced to sell.',
 18000.00, 'SELL', 'GOOD', NULL, 1, 'Rajpur Road',
 '["https://picsum.photos/seed/staymart-dining1/800/600","https://picsum.photos/seed/staymart-dining2/800/600"]', 'APPROVED', TRUE, 60, DATE_SUB(NOW(), INTERVAL 5 DAY)),

(10, 3, 9, 'Double Bed with Storage (Queen)',
 'Queen size double bed with hydraulic storage, engineered wood in walnut finish. Mattress can be included at extra cost.',
 12000.00, 'SELL', 'GOOD', 'Nilkamal', 7, 'Sahastradhara Road',
 '["https://picsum.photos/seed/staymart-bed1/800/600","https://picsum.photos/seed/staymart-bed2/800/600"]', 'APPROVED', TRUE, 88, DATE_SUB(NOW(), INTERVAL 9 DAY)),

(11, 4, 9, '3-Seater Fabric Sofa (Grey)',
 'Comfortable 3-seater fabric sofa, grey, 2 years old. No tears or stains, cushions firm. Pick up from Patel Nagar.',
 15500.00, 'SELL', 'GOOD', NULL, 4, 'Patel Nagar',
 '["https://picsum.photos/seed/staymart-sofa1/800/600","https://picsum.photos/seed/staymart-sofa2/800/600"]', 'APPROVED', TRUE, 70, DATE_SUB(NOW(), INTERVAL 11 DAY)),

-- Books & Stationery (category 10)
(12, 5, 10, 'HC Verma + NCERT PCM Set (Class 12)',
 'Complete JEE prep set: HC Verma Vol 1 and 2, NCERT Physics, Chemistry and Maths. Neatly kept, no torn pages.',
 900.00, 'SELL', 'GOOD', NULL, 4, 'Patel Nagar',
 '["https://picsum.photos/seed/staymart-books1/800/600"]', 'APPROVED', TRUE, 55, DATE_SUB(NOW(), INTERVAL 4 DAY)),

(13, 2, 10, 'GATE CSE Standard Books + Notes',
 'Full GATE CSE set - CLRS, Galvin OS, Korth DBMS, Tanenbaum Networks plus handwritten Made Easy notes.',
 1800.00, 'SELL', 'GOOD', NULL, 3, 'ISBT',
 '["https://picsum.photos/seed/staymart-gate1/800/600","https://picsum.photos/seed/staymart-gate2/800/600"]', 'APPROVED', TRUE, 130, DATE_SUB(NOW(), INTERVAL 13 DAY)),

-- Home Appliances (category 11)
(14, 3, 11, 'LG 6.5kg Semi-Automatic Washing Machine',
 'LG 6.5kg semi-automatic washing machine, works perfectly. Selling due to relocation. With original manual.',
 7500.00, 'SELL', 'GOOD', 'LG', 5, 'Kaonli',
 '["https://picsum.photos/seed/staymart-wm1/800/600","https://picsum.photos/seed/staymart-wm2/800/600"]', 'APPROVED', TRUE, 95, DATE_SUB(NOW(), INTERVAL 6 DAY)),

(15, 4, 11, 'Samsung 253L Double Door Refrigerator',
 'Samsung 253L frost-free double door fridge, 3 star. Cooling excellent, no dents. Bought 2021.',
 13000.00, 'SELL', 'GOOD', 'Samsung', 1, 'Rajpur Road',
 '["https://picsum.photos/seed/staymart-fridge1/800/600","https://picsum.photos/seed/staymart-fridge2/800/600"]', 'APPROVED', TRUE, 110, DATE_SUB(NOW(), INTERVAL 8 DAY)),

(16, 5, 11, 'Havells 1.5 Ton Split AC (3 Star)',
 'Havells 1.5 ton split AC, cooling coil recently serviced. Cosmetically fair, works well. Indoor and outdoor unit included.',
 16000.00, 'SELL', 'FAIR', 'Havells', 7, 'Sahastradhara Road',
 '["https://picsum.photos/seed/staymart-ac1/800/600","https://picsum.photos/seed/staymart-ac2/800/600"]', 'APPROVED', TRUE, 150, DATE_SUB(NOW(), INTERVAL 14 DAY)),

(17, 2, 11, 'Philips 1000W Mixer Grinder',
 'Philips HL7756 mixer grinder with 3 jars, 1000W. Motor powerful, jars in good condition.',
 2200.00, 'SELL', 'GOOD', 'Philips', 6, 'Ballupur',
 '["https://picsum.photos/seed/staymart-mixer1/800/600"]', 'APPROVED', TRUE, 40, DATE_SUB(NOW(), INTERVAL 3 DAY)),

-- Vehicles (category 12)
(18, 3, 12, 'Honda Activa 6G (2021)',
 'Honda Activa 6G 2021, single owner, 18,000 km driven. Insurance valid till next year, all papers clear.',
 58000.00, 'SELL', 'GOOD', 'Honda', 3, 'ISBT',
 '["https://picsum.photos/seed/staymart-activa1/800/600","https://picsum.photos/seed/staymart-activa2/800/600"]', 'APPROVED', TRUE, 300, DATE_SUB(NOW(), INTERVAL 2 DAY)),

(19, 4, 12, 'Royal Enfield Classic 350 (2019)',
 'Royal Enfield Classic 350, gunmetal grey, 2019 model. Well maintained, new tyres and battery. Genuine buyers only.',
 98000.00, 'SELL', 'GOOD', 'Royal Enfield', 2, 'Clock Tower',
 '["https://picsum.photos/seed/staymart-re1/800/600","https://picsum.photos/seed/staymart-re2/800/600"]', 'APPROVED', TRUE, 480, DATE_SUB(NOW(), INTERVAL 5 DAY)),

(20, 5, 12, 'Bajaj Pulsar 150 (2020)',
 'Bajaj Pulsar 150 twin disc, 2020, 24,000 km. Regular servicing done, smooth engine. Transfer support provided.',
 62000.00, 'SELL', 'GOOD', 'Bajaj', 4, 'Patel Nagar',
 '["https://picsum.photos/seed/staymart-pulsar1/800/600","https://picsum.photos/seed/staymart-pulsar2/800/600"]', 'APPROVED', TRUE, 220, DATE_SUB(NOW(), INTERVAL 10 DAY)),

-- Sports & Fitness (category 13)
(21, 2, 13, 'Yonex Badminton Racket Set + Shuttles',
 'Pair of Yonex badminton rackets with cover and a tube of shuttles. Great condition, barely used. Available on rent too.',
 2800.00, 'RENT', 'GOOD', 'Yonex', 6, 'Ballupur',
 '["https://picsum.photos/seed/staymart-badminton1/800/600"]', 'APPROVED', TRUE, 65, DATE_SUB(NOW(), INTERVAL 4 DAY)),

(22, 3, 13, 'Cosco Cricket Kit (Full)',
 'Complete Cosco cricket kit - bat, pads, gloves, helmet, thigh guard and kit bag. Suitable for tennis ball and leather ball.',
 4500.00, 'SELL', 'GOOD', 'Cosco', 5, 'Kaonli',
 '["https://picsum.photos/seed/staymart-cricket1/800/600","https://picsum.photos/seed/staymart-cricket2/800/600"]', 'APPROVED', TRUE, 80, DATE_SUB(NOW(), INTERVAL 12 DAY)),

-- Fashion (category 15)
(23, 4, 15, 'Levis Denim Jacket (Size L)',
 'Genuine Levis denim jacket, size L, worn a few times. Classic blue wash, all buttons intact.',
 1500.00, 'SELL', 'GOOD', 'Levis', 1, 'Rajpur Road',
 '["https://picsum.photos/seed/staymart-jacket1/800/600"]', 'APPROVED', TRUE, 44, DATE_SUB(NOW(), INTERVAL 3 DAY)),

-- Others (category 16)
(24, 5, 16, 'Godrej 2-Door Steel Almirah',
 'Godrej 2-door steel almirah with locker, powder-coated grey. Good storage, minor scratches. Buyer to arrange transport.',
 6000.00, 'SELL', 'GOOD', 'Godrej', 5, 'Kaonli',
 '["https://picsum.photos/seed/staymart-almirah1/800/600","https://picsum.photos/seed/staymart-almirah2/800/600"]', 'APPROVED', TRUE, 85, DATE_SUB(NOW(), INTERVAL 7 DAY));
