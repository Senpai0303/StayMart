-- StayMart seed data: locations and categories
USE staymart;

INSERT INTO locations (city, area, state, pincode, latitude, longitude) VALUES
('Dehradun', 'Rajpur Road', 'Uttarakhand', '248001', 30.3165, 78.0322),
('Dehradun', 'Clock Tower', 'Uttarakhand', '248001', 30.3245, 78.0339),
('Dehradun', 'ISBT', 'Uttarakhand', '248001', 30.2898, 78.0493),
('Dehradun', 'Patel Nagar', 'Uttarakhand', '248001', 30.3022, 78.0480),
('Dehradun', 'Kaonli', 'Uttarakhand', '248001', 30.2800, 78.0700),
('Dehradun', 'Ballupur', 'Uttarakhand', '248001', 30.3280, 78.0600),
('Dehradun', 'Sahastradhara Road', 'Uttarakhand', '248001', 30.3600, 78.0900),
('Dehradun', 'Raipur Road', 'Uttarakhand', '248008', 30.2958, 78.0783),
('Rishikesh', 'Laxman Jhula', 'Uttarakhand', '249302', 30.1290, 78.3220),
('Rishikesh', 'Tapovan', 'Uttarakhand', '249192', 30.1500, 78.3400),
('Haridwar', 'Har Ki Pauri', 'Uttarakhand', '249401', 29.9457, 78.1642),
('Haridwar', 'SIDCUL', 'Uttarakhand', '249403', 29.9200, 78.1800),
('Mussoorie', 'Mall Road', 'Uttarakhand', '248179', 30.4520, 78.0640),
('Nainital', 'Mall Road', 'Uttarakhand', '263001', 29.3919, 79.4542),
('Roorkee', 'Civil Lines', 'Uttarakhand', '247667', 29.8543, 77.8880);

INSERT INTO categories (name, type, icon) VALUES
('PG', 'ACCOMMODATION', '🏠'),
('Hostel', 'ACCOMMODATION', '🏨'),
('Flat', 'ACCOMMODATION', '🏢'),
('Room', 'ACCOMMODATION', '🛏️'),
('Hotel', 'ACCOMMODATION', '🏩'),
('Dormitory', 'ACCOMMODATION', '🛌'),
('Electronics', 'PRODUCT', '💻'),
('Mobile Phones', 'PRODUCT', '📱'),
('Furniture', 'PRODUCT', '🪑'),
('Books & Stationery', 'PRODUCT', '📚'),
('Home Appliances', 'PRODUCT', '🧺'),
('Vehicles', 'PRODUCT', '🏍️'),
('Sports & Fitness', 'PRODUCT', '🏏'),
('Home & Kitchen', 'PRODUCT', '🍳'),
('Fashion', 'PRODUCT', '👕'),
('Others', 'PRODUCT', '📦');
