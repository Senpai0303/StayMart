
USE staymart;

-- UPDATE PROPERTIES WITH REALISTIC CLASSIFIED TITLES & DESCRIPTIONS
UPDATE properties SET 
  title = 'Sunrise Boys PG (Near Graphic Era University & ISBT)',
  description = 'Well-maintained Boys PG located within 800m of Graphic Era (GEU) & ISBT Dehradun. 
• 3 times nutritious homestyle meals included (breakfast, lunch/tiffin, dinner).
• High-speed 100 Mbps WiFi & 24/7 power backup with inverter.
• Hot water geyser in attached washrooms, RO drinking water on each floor.
• Daily room cleaning and CCTV security. Rent includes electricity and water charges.',
  area = 'Clement Town'
WHERE id = 1;

UPDATE properties SET 
  title = 'Green Valley Luxury Girls PG, Rajpur Road',
  description = 'Premium Girls PG on Rajpur Road near Pacific Mall. Highly secure residential area with biometric entry and female warden.
• Fully furnished with box beds, study table, ergonomic chair, and full-length wooden almirah.
• Fresh hygienic meals (North & South Indian options).
• Air conditioner and water purifier installed. 
• 5 mins walking distance to local cafes and transport.',
  area = 'Rajpur Road'
WHERE id = 2;

UPDATE properties SET 
  title = 'Comfort Student Hostel, Ballupur Chowk',
  description = 'Affordable and peaceful student hostel near Ballupur Chowk, close to FRI and Wadia Institute.
• Twin sharing and triple sharing spacious rooms.
• Dedicated quiet study hall and high-speed fiber internet.
• Wholesome mess meals with weekend special menus.
• Washing machine available for student laundry. Zero brokerage.',
  area = 'Ballupur'
WHERE id = 3;

UPDATE properties SET 
  title = 'Tapovan Backpacker & Digital Nomad Co-living, Rishikesh',
  description = 'Co-living space overlooking the serene hills of Tapovan, Rishikesh.
• Ergonomic coworking spaces with 200 Mbps dual-line internet.
• Community rooftop cafe with mountain and Ganga river views.
• Weekly yoga sessions, shared kitchen, and personal keycard lockers.
• Ideal for remote professionals and long-term travelers.',
  area = 'Tapovan'
WHERE id = 4;

UPDATE properties SET 
  title = 'Budget Single Room for Boys, Patel Nagar',
  description = 'Independent single room with attached private bathroom in Patel Nagar.
• Equipped with single wooden cot, mattress, study desk, and ceiling fan.
• Geyser installed in washroom. Independent sub-meter for electricity.
• Close to coaching centers, libraries, and local bus stand. No landlord interference.',
  area = 'Patel Nagar'
WHERE id = 5;

UPDATE properties SET 
  title = 'Furnished 1BHK Flat with Balcony, Subhash Nagar',
  description = 'Ready-to-move-in fully furnished 1BHK apartment in Subhash Nagar near Graphic Era Hill University.
• Bedroom with queen bed, wardrobe, and AC.
• Living room with 3-seater sofa and coffee table.
• Fully equipped modular kitchen with gas cylinder, stove, and double-door refrigerator.
• Private balcony with sunset view. Gated parking available.',
  area = 'Subhash Nagar'
WHERE id = 6;

UPDATE properties SET 
  title = 'Spacious 2BHK Mountain View Apartment, Sahastradhara Road',
  description = 'Luxurious 2BHK residential flat in a peaceful gated society on Sahastradhara Road.
• 2 large bedrooms with 2 attached modern bathrooms and 2 panoramic balconies facing Mussoorie hills.
• Modular kitchen with chimney and piped gas connection.
• Society amenities: 24/7 security guard, automatic lift, covered car parking, and gym.',
  area = 'Sahastradhara Road'
WHERE id = 7;

UPDATE properties SET 
  title = 'Budget Guest Rooms & Student Long-Stay (Clock Tower Dehradun)',
  description = 'Centrally located guest rooms near Clock Tower and Paltan Bazar for outstation entrance exam takers, visiting parents, and student short stays.
• Equipped with work/study desk, comfortable bed, and clean attached bathroom.
• Fast Wi-Fi, 24-hour hot water supply, and easy walking access to local transit.
• Economical daily and monthly rates with zero brokerage.',
  area = 'Clock Tower'
WHERE id = 8;

UPDATE properties SET 
  title = 'Ganga View Dormitory Bed for Students & Pilgrims, Haridwar',
  description = 'Air-conditioned dormitory located within 300 meters of Har Ki Pauri ghat.
• Clean bunk beds with fresh sanitized linen, reading lamp, and charging sockets.
• Personal metal locker for luggage safety. 24/7 hot water supply.
• Budget-friendly option for weekend visitors, students, and pilgrims.',
  area = 'Har Ki Pauri'
WHERE id = 9;

UPDATE properties SET 
  title = 'Modern Co-living Studio Apartment, Kaonli Chowk',
  description = 'Chic studio apartment with contemporary interior decor near Kaonli Chowk / Balliwala.
• Combined bedroom and living zone with kitchenette, induction cooktop, and microwave.
• Smart Android TV with OTT subscriptions included in rent.
• High-speed fiber WiFi, power backup, and dedicated two-wheeler parking.',
  area = 'Kaonli'
WHERE id = 10;

UPDATE properties SET 
  title = 'Cloud 9 Hill View PG & Homestay, Mussoorie Mall Road',
  description = 'Charming homestay and long-term PG situated right off Mall Road, Mussoorie.
• Traditional wooden paneling with room heater and valley view windows.
• Home-cooked Garhwali and North Indian meals.
• Peaceful atmosphere suitable for creative work, study, and relaxed living in the hills.',
  area = 'Mall Road'
WHERE id = 11;

UPDATE properties SET 
  title = 'Working Women & Student PG, Roorkee Civil Lines',
  description = 'Safe and secure residence for female students and professionals in Civil Lines, Roorkee.
• Walking distance to IIT Roorkee main gate.
• Nutritious 3-time meals, RO drinking water, and high-speed internet.
• CCTV surveillance, biometric security, and dedicated full-time caretaker.',
  area = 'Civil Lines'
WHERE id = 12;

-- UPDATE PRODUCTS WITH AUTHENTIC OLX / AMAZON STYLE DETAILS
UPDATE products SET 
  title = 'Dell Inspiron 15 3511 Laptop Core i5 11th Gen (16GB/512GB SSD)',
  description = 'Purchased for engineering college coursework at Graphic Era. Upgrading to a desktop setup.
• Processor: Intel Core i5-1135G7 (11th Gen) up to 4.2 GHz.
• RAM & Storage: Upgraded to 16 GB DDR4 RAM + 512 GB M.2 PCIe NVMe SSD (boots in 5 seconds).
• Display: 15.6-inch Full HD Anti-Glare WVA display.
• Battery health: Excellent (gives 4.5+ hours backup).
• Condition: Mint condition, zero dents or scratches. Screen protector on since Day 1.
• Inclusions: Original Dell 65W charger, original retail box, and purchase invoice.',
  brand = 'Dell',
  price = 32500.00,
  area = 'Clement Town'
WHERE id = 1;

UPDATE products SET 
  title = 'HP Pavilion Gaming 15 Laptop (Ryzen 5 5600H / GTX 1650 / 144Hz)',
  description = 'Selling my gaming laptop used primarily for CAD software and casual GTA V gaming.
• Processor: AMD Ryzen 5 5600H (6 Cores / 12 Threads).
• GPU: NVIDIA GeForce GTX 1650 (4GB GDDR6 dedicated graphics).
• Screen: 15.6-inch 144Hz FHD IPS display with micro-edge bezels.
• RAM & Storage: 8 GB DDR4 (expandable) + 512 GB NVMe SSD.
• Inclusions: Original HP 150W high-speed charger. Thermal paste freshly serviced last month.',
  brand = 'HP',
  price = 39500.00,
  area = 'Ballupur'
WHERE id = 2;

UPDATE products SET 
  title = 'Apple MacBook Air M1 2020 (8GB/256GB SSD) Space Grey',
  description = 'Genuine Apple MacBook Air M1 chip in pristine Space Grey color.
• Battery Health: 92% with only 148 charge cycles (lasts 12-14 hours on a single charge).
• Performance: Extremely fast for coding, video editing, and college assignments. Zero fan noise.
• Inclusions: Original Apple 30W USB-C power adapter, USB-C braided cable, and original box.
• Bill available. Reason for sale: Office provided a work MacBook Pro.',
  brand = 'Apple',
  price = 56000.00,
  area = 'Rajpur Road'
WHERE id = 3;

UPDATE products SET 
  title = 'Canon EOS 1500D 24.1MP DSLR Camera + 18-55mm IS II Lens + 64GB Card',
  description = 'Purchased for a photography club project at Doon University. Barely used (shutter count under 3,200).
• Sensor: 24.1 Megapixel APS-C CMOS sensor with DIGIC 4+ processor.
• Built-in Wi-Fi & NFC for instant photo transfer to smartphone.
• Includes: EF-S 18-55mm f/3.5-5.6 IS II Image Stabilizer lens, original battery, wall charger, SanDisk 64GB Extreme SD card, lens cap, and padded Canon shoulder bag.
• Tested and works like brand new.',
  brand = 'Canon',
  price = 21500.00,
  area = 'Clock Tower'
WHERE id = 4;

UPDATE products SET 
  title = 'Apple iPhone 12 128GB (Pacific Blue) - With Bill, Box & Cable',
  description = 'Single owner iPhone 12 in striking Pacific Blue. Never opened or repaired.
• Storage: 128 GB (plenty of room for photos and 4K Dolby Vision videos).
• Battery Health: 87% (comfortably lasts the whole day).
• Face ID, TrueTone, and all cameras function flawlessly.
• Always used with Spigen tempered glass and silicone back case.
• Inclusions: Original box matching IMEI, USB-C to Lightning cable, and Spigen case.',
  brand = 'Apple',
  price = 29500.00,
  area = 'Rajpur Road'
WHERE id = 5;

UPDATE products SET 
  title = 'Samsung Galaxy S21 5G 128GB (Phantom Grey) - Dual SIM',
  description = 'Flagship Samsung phone with Dynamic AMOLED 2X 120Hz display and pro-grade triple camera.
• Condition: Very clean, no screen burn-in or frame scratches.
• Features: 8GB RAM, 128GB Storage, 8K video recording, wireless charging, and IP68 water resistance.
• Inclusions: Type-C fast charging cable, SIM ejector tool, and premium Ringke matte case.',
  brand = 'Samsung',
  price = 24000.00,
  area = 'ISBT'
WHERE id = 6;

UPDATE products SET 
  title = 'Redmi Note 12 Pro 5G 128GB (Onyx Black) - 67W Charger Included',
  description = 'Solid 5G smartphone with flagship 50MP Sony IMX766 sensor with Optical Image Stabilization (OIS).
• 120Hz Pro AMOLED Dolby Vision display.
• Superfast 67W Turbo Charger included in box (charges 0-100% in 45 minutes).
• Just 7 months old, original invoice from Mi Store available. Scratchless condition.',
  brand = 'Xiaomi',
  price = 13500.00,
  area = 'Kaonli'
WHERE id = 7;

UPDATE products SET 
  title = 'OnePlus Nord CE 2 Lite 5G 128GB (Black Dusk) - 8GB RAM',
  description = 'Clean and snappy 5G phone running clean OxygenOS 14.
• Big 5000 mAh battery with 33W SuperVOOC fast charging (lasts 1.5 days easily).
• 64 MP AI Triple camera and 120Hz smooth refresh rate.
• Reason for selling: Upgraded to OnePlus 12R. Comes with original charger, cable, and box.',
  brand = 'OnePlus',
  price = 10500.00,
  area = 'Subhash Nagar'
WHERE id = 8;

UPDATE products SET 
  title = 'Student Wooden Study Desk + Ergonomic Mesh Chair Combo',
  description = 'Sturdy engineered wood study desk (3.5x2 ft) with drawer and cable grommet, paired with Green Soul breathable mid-back mesh chair.
• Perfect for long coding sprints and exam preparation.
• Graduating senior moving out of Clement Town.
• Dimensions: Desk 42" W x 24" D x 30" H. Chair with adjustable lumbar support.',
  brand = 'Green Soul',
  price = 3200.00,
  area = 'Rajpur Road'
WHERE id = 9;

UPDATE products SET 
  title = 'Single Wooden Bed Cot (3x6 ft) + 5-Inch Foam Mattress',
  description = 'Solid ply-board base single cot (3x6 ft) with Wakefit 5-inch orthopedic foam mattress and washable cover.
• Compact fit for any student PG room.
• Easily disassembles into 4 panels in 10 minutes for quick transport.
• Clean, stain-free mattress used with waterproof protector.',
  brand = 'Wakefit',
  price = 3800.00,
  area = 'Sahastradhara Road'
WHERE id = 10;

UPDATE products SET 
  title = 'Foldable Bed Study Table + XL Leatherette Bean Bag Combo',
  description = 'Compact foldable bed study table with tablet groove and cup holder, plus an XL brown leatherette bean bag filled with fresh beans.
• Great for late-night assignments, laptop work, and hostel room reading.
• Both items in clean, gently used condition.',
  brand = 'Generic',
  price = 1400.00,
  area = 'Patel Nagar'
WHERE id = 11;

UPDATE products SET 
  title = 'Class 11 & 12 JEE / Engineering Physics & Chemistry Bundle',
  description = 'Complete study material set for Class 11 & 12 / JEE Main & Advanced:
• HC Verma Concepts of Physics Volume 1 & Volume 2 (Latest Edition).
• NCERT Physics, Chemistry, and Mathematics (Part 1 & 2 complete).
• DC Pandey Mechanics Vol 1 & 2 included as free bonus.
• Clean pages, no missing sheets, formulas highlighted neatly. Cracked JEE, selling to juniors.',
  brand = 'Bharati Bhawan',
  price = 950.00,
  area = 'Patel Nagar'
WHERE id = 12;

UPDATE products SET 
  title = 'GATE CSE & IT Complete Notes (Made Easy) + 15 Years Solved Papers',
  description = 'Comprehensive preparation package for GATE CSE:
• Made Easy classroom handwritten notes for all 10 core subjects (OS, DBMS, CN, Algorithms, TOC, Compiler, COA, DS, Discrete Maths, Digital).
• 15 Years Chapter-wise solved question papers with detailed answer explanations.
• Standard reference books notes summary. Extremely helpful for scoring top AIR.',
  brand = 'Made Easy',
  price = 1600.00,
  area = 'Clement Town'
WHERE id = 13;

UPDATE products SET 
  title = 'Symphony Diet 35T Personal Tower Air Cooler with Stand & Trolley',
  description = '35-litre compact tower cooler with honeycomb pads and 4-wheel castor trolley.
• Low power consumption (170W) runs smoothly on student PG inverters during Dehradun summer heat.
• Features powerful blower, ice chamber, and water level indicator.
• Senior passing out, fully functional and cleaned.',
  brand = 'Symphony',
  price = 2400.00,
  area = 'Kaonli'
WHERE id = 14;

UPDATE products SET 
  title = 'Whirlpool 190L Single Door Refrigerator (Direct Cool, 4-Star)',
  description = 'Kept in a 2-student shared flat near Clement Town. Excellent cooling for summer drinks, water, and milk.
• 4-star energy rating adds barely ₹200 to monthly electricity bill.
• Direct cool with fast ice-making compartment.
• Clean, odor-free, 100% working cooling condition.',
  brand = 'Whirlpool',
  price = 6500.00,
  area = 'Rajpur Road'
WHERE id = 15;

UPDATE products SET 
  title = 'Winter Room Essentials: Bajaj 2000W Radiant Heater + Electric Kettle',
  description = 'Bajaj 2000W halogen radiant room heater heats small rooms within 10 minutes for chilly Dehradun winters.
• Paired with a Prestige 1.5L cordless electric kettle for midnight Maggi, coffee, and tea.
• Both appliances in excellent working condition with original power cords.',
  brand = 'Bajaj',
  price = 1100.00,
  area = 'Sahastradhara Road'
WHERE id = 16;

UPDATE products SET 
  title = 'Prestige 1600W Induction Cooktop + Non-Stick Frying Pan & Pot',
  description = 'Allowed in student PGs where LPG cylinders are restricted.
• Push-button Indian menu presets (milk, boil, fry, chapati).
• Includes non-stick frying pan and stainless steel boiling pot with glass lid.
• Only 6 months old, clean condition and works flawlessly.',
  brand = 'Prestige',
  price = 1500.00,
  area = 'Ballupur'
WHERE id = 17;

UPDATE products SET 
  title = 'Honda Activa 6G (2021, UK-07 Passing) - Senior Moving Out',
  description = 'Single-hand driven Honda Activa 6G in Matte Axis Grey metallic color.
• Odometer: 9,450 km genuine reading.
• Mileage: Delivers 50-52 kmpl in Dehradun city traffic.
• Condition: Excellent engine sound, smooth self-start, both tubeless tyres in 80% life.
• All documents complete: Original RC (UK-07 passing), valid insurance till Nov 2026, and PUC.
• Ready for instant name transfer. Reason for sale: Moving out after graduation.',
  brand = 'Honda',
  price = 52000.00,
  area = 'ISBT'
WHERE id = 18;

UPDATE products SET 
  title = 'Royal Enfield Classic 350 Stealth Black (2019 Dual ABS)',
  description = 'Iconic Royal Enfield Classic 350 in Matte Stealth Black edition with dual-channel ABS.
• Single owner, carefully maintained with timely authorized service records.
• Driven: 14,200 km mostly on Dehradun-Rishikesh highway.
• Equipped with crash guard with rope wrap, comfortable touring seat, and hazard light module.
• Smooth thumping engine, zero oil leaks, brand new Exide battery with 3 years warranty.
• Test ride welcome in Clock Tower / Paltan Bazar area.',
  brand = 'Royal Enfield',
  price = 95000.00,
  area = 'Clock Tower'
WHERE id = 19;

UPDATE products SET 
  title = 'Hero Sprint Pro 21-Speed Geared Mountain Bicycle with Number Lock',
  description = '21-speed Shimano derailleur and shifters, front telescopic suspension, and dual disc brakes.
• Saves daily auto fare between Clement Town and Graphic Era campus.
• Serviced 3 weeks ago with new brake pads and smooth chain lube.
• Includes sturdy combination cable lock and bottle cage.',
  brand = 'Hero',
  price = 4500.00,
  area = 'Patel Nagar'
WHERE id = 20;

UPDATE products SET 
  title = 'Yonex Nanoray 18i Carbon Graphite Racket + Shuttles Tube',
  description = 'Authentic Yonex Nanoray 18i (77g ultra-lightweight carbon graphite racket).
• Strung with Yonex BG-65 string at 24 lbs tension for quick handling and control.
• Includes: Full padded Yonex thermal cover, brand new towel grip, and half tube of Yonex Mavis 350 nylon shuttles.
• No frame cracks or paint chips.',
  brand = 'Yonex',
  price = 2200.00,
  area = 'Ballupur'
WHERE id = 21;

UPDATE products SET 
  title = 'First-Year Engineering Drawing (ED) Complete Kit + White Lab Apron',
  description = 'Essential first-year kit for B.Tech students:
• Omega mini-drafter with carry pouch and clamping knob in perfect condition.
• Imperial drawing board, sheet container tube, 45° and 60° set squares, roller scale, and French curves.
• Includes size 38 white cotton chemistry/workshop lab coat in clean condition.',
  brand = 'Omega',
  price = 1200.00,
  area = 'Kaonli'
WHERE id = 22;

UPDATE products SET 
  title = 'Levis Original Trucker Denim Jacket (Size L) - Dark Indigo Blue',
  description = 'Authentic 100% cotton heavy denim trucker jacket from Levis (purchased from Pacific Mall Dehradun).
• Color: Dark Indigo Blue with contrast golden stitching and metal shank buttons.
• Size: Men''s Large (40-42 chest).
• Condition: Worn only 2 times during winter festival, zero fading or fabric defects.
• Retails for ₹4,999 on Myntra/Amazon.',
  brand = 'Levis',
  price = 1400.00,
  area = 'Rajpur Road'
WHERE id = 23;

UPDATE products SET 
  title = 'Collapsible 4-Tier Portable Clothes Wardrobe with Dust Cover',
  description = 'Powder-coated steel pipe frame with zipped dustproof fabric cover and 4 tier fabric shelves.
• Assembles in 10 minutes without tools.
• Holds 25+ shirts, winter jackets, and study bags.
• Folds completely flat to carry easily on a scooty or auto.',
  brand = 'Generic',
  price = 950.00,
  area = 'Kaonli'
WHERE id = 24;
