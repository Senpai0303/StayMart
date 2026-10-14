-- StayMart database schema (MySQL 8)
CREATE DATABASE IF NOT EXISTS staymart
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE staymart;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS user_behaviors;
DROP TABLE IF EXISTS chats;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS wishlists;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. users
CREATE TABLE users (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone         VARCHAR(15),
    role          ENUM('ADMIN','USER') DEFAULT 'USER',
    profile_pic   VARCHAR(255),
    city          VARCHAR(100) DEFAULT 'Dehradun',
    state         VARCHAR(100) DEFAULT 'Uttarakhand',
    bio           TEXT NULL,
    is_active     BOOLEAN DEFAULT TRUE,
    is_verified   BOOLEAN DEFAULT FALSE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. locations
CREATE TABLE locations (
    id        BIGINT AUTO_INCREMENT PRIMARY KEY,
    city      VARCHAR(100) NOT NULL,
    area      VARCHAR(100),
    state     VARCHAR(100) DEFAULT 'Uttarakhand',
    pincode   VARCHAR(10),
    latitude  DECIMAL(10,8),
    longitude DECIMAL(11,8)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. categories
CREATE TABLE categories (
    id        BIGINT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    type      ENUM('ACCOMMODATION','PRODUCT') NOT NULL,
    icon      VARCHAR(50),
    parent_id BIGINT NULL,
    CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. properties
CREATE TABLE properties (
    id                BIGINT AUTO_INCREMENT PRIMARY KEY,
    posted_by         BIGINT NOT NULL,
    title             VARCHAR(200) NOT NULL,
    description       TEXT,
    type              ENUM('PG','ROOM','HOSTEL','HOTEL','FLAT','DORMITORY') NOT NULL,
    gender_preference ENUM('MALE','FEMALE','ANY') DEFAULT 'ANY',
    address           VARCHAR(255),
    area              VARCHAR(100),
    location_id       BIGINT,
    price_per_month   DECIMAL(10,2),
    deposit_amount    DECIMAL(10,2) DEFAULT 0,
    amenities         JSON,
    total_rooms       INT DEFAULT 1,
    available_rooms   INT DEFAULT 1,
    images            JSON,
    status            ENUM('PENDING','APPROVED','REJECTED') DEFAULT 'PENDING',
    is_available      BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_property_user FOREIGN KEY (posted_by) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_property_location FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL,
    INDEX idx_property_status (status),
    INDEX idx_property_type (type),
    INDEX idx_property_area (area),
    INDEX idx_property_location (location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. rooms
CREATE TABLE rooms (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    property_id  BIGINT NOT NULL,
    room_number  VARCHAR(20),
    type         ENUM('SINGLE','DOUBLE','TRIPLE','DORMITORY') NOT NULL,
    price        DECIMAL(10,2),
    capacity     INT DEFAULT 1,
    floor_number INT DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    images       JSON,
    CONSTRAINT fk_room_property FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    INDEX idx_room_property (property_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. products
CREATE TABLE products (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    posted_by    BIGINT NOT NULL,
    category_id  BIGINT,
    title        VARCHAR(200) NOT NULL,
    description  TEXT,
    price        DECIMAL(10,2) NOT NULL,
    listing_type ENUM('SELL','RENT','BOTH') DEFAULT 'SELL',
    `condition`  ENUM('NEW','LIKE_NEW','GOOD','FAIR','OLD') DEFAULT 'GOOD',
    brand        VARCHAR(100) NULL,
    location_id  BIGINT,
    area         VARCHAR(100),
    images       JSON,
    status       ENUM('PENDING','APPROVED','REJECTED') DEFAULT 'PENDING',
    is_available BOOLEAN DEFAULT TRUE,
    views_count  INT DEFAULT 0,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_user FOREIGN KEY (posted_by) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_product_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    CONSTRAINT fk_product_location FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL,
    INDEX idx_product_status (status),
    INDEX idx_product_category (category_id),
    INDEX idx_product_area (area),
    INDEX idx_product_location (location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. bookings
CREATE TABLE bookings (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    booker_id    BIGINT NOT NULL,
    property_id  BIGINT NOT NULL,
    room_id      BIGINT NULL,
    check_in     DATE NOT NULL,
    check_out    DATE NULL,
    total_amount DECIMAL(10,2),
    months       INT DEFAULT 1,
    status       ENUM('PENDING','CONFIRMED','CANCELLED','COMPLETED') DEFAULT 'PENDING',
    message      TEXT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_booking_booker FOREIGN KEY (booker_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_booking_property FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    CONSTRAINT fk_booking_room FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL,
    INDEX idx_booking_booker (booker_id),
    INDEX idx_booking_property (property_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. orders
CREATE TABLE orders (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    buyer_id   BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    seller_id  BIGINT NOT NULL,
    quantity   INT DEFAULT 1,
    amount     DECIMAL(10,2),
    order_type ENUM('BUY','RENT') DEFAULT 'BUY',
    rent_start DATE NULL,
    rent_end   DATE NULL,
    status     ENUM('PENDING','CONFIRMED','COMPLETED','CANCELLED') DEFAULT 'PENDING',
    message    TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_buyer FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_order_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_order_seller FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_order_buyer (buyer_id),
    INDEX idx_order_seller (seller_id),
    INDEX idx_order_product (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. wishlists
CREATE TABLE wishlists (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id    BIGINT NOT NULL,
    item_type  ENUM('PROPERTY','PRODUCT') NOT NULL,
    item_id    BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_wishlist_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_wishlist (user_id, item_type, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. reviews
CREATE TABLE reviews (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    reviewer_id BIGINT NOT NULL,
    item_type   ENUM('PROPERTY','PRODUCT','USER') NOT NULL,
    item_id     BIGINT NOT NULL,
    rating      INT NOT NULL,
    comment     TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_user FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_review_rating CHECK (rating BETWEEN 1 AND 5),
    INDEX idx_review_item (item_type, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. chats
CREATE TABLE chats (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    sender_id    BIGINT NOT NULL,
    receiver_id  BIGINT NOT NULL,
    listing_type ENUM('PROPERTY','PRODUCT') NULL,
    listing_id   BIGINT NULL,
    message      TEXT NOT NULL,
    `timestamp`  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read      BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_chat_sender FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_chat_receiver FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_chat_sender (sender_id),
    INDEX idx_chat_receiver (receiver_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. user_behaviors
CREATE TABLE user_behaviors (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id      BIGINT NOT NULL,
    item_type    ENUM('PROPERTY','PRODUCT') NOT NULL,
    item_id      BIGINT NOT NULL,
    action       ENUM('VIEW','SEARCH','WISHLIST','BOOK','ORDER','CONTACT') NOT NULL,
    `timestamp`  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    search_query VARCHAR(255) NULL,
    city_filter  VARCHAR(100) NULL,
    CONSTRAINT fk_behavior_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_behavior_user (user_id),
    INDEX idx_behavior_item (item_type, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
