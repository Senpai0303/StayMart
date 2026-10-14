package com.staymart.config;

import com.staymart.entity.Category;
import com.staymart.entity.User;
import com.staymart.entity.enums.CategoryType;
import com.staymart.entity.enums.Role;
import com.staymart.repository.CategoryRepository;
import com.staymart.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Component
public class DataSeeder implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataSeeder.class);

    private final UserRepository userRepository;
    private final CategoryRepository categoryRepository;
    private final PasswordEncoder passwordEncoder;
    private final String adminEmail;
    private final String adminPassword;
    private final String adminName;

    public DataSeeder(UserRepository userRepository,
                      CategoryRepository categoryRepository,
                      PasswordEncoder passwordEncoder,
                      @Value("${app.seed.admin-email}") String adminEmail,
                      @Value("${app.seed.admin-password}") String adminPassword,
                      @Value("${app.seed.admin-name}") String adminName) {
        this.userRepository = userRepository;
        this.categoryRepository = categoryRepository;
        this.passwordEncoder = passwordEncoder;
        this.adminEmail = adminEmail;
        this.adminPassword = adminPassword;
        this.adminName = adminName;
    }

    @Override
    @Transactional
    public void run(String... args) {
        seedCategories();
        seedAdmin();
        log.info("StayMart data seeding completed");
    }

    private void seedCategories() {
        if (categoryRepository.count() > 0) {
            return;
        }
        List<Category> categories = List.of(
                Category.builder().name("PG").type(CategoryType.ACCOMMODATION).icon("🏠").build(),
                Category.builder().name("Hostel").type(CategoryType.ACCOMMODATION).icon("🏨").build(),
                Category.builder().name("Flat").type(CategoryType.ACCOMMODATION).icon("🏢").build(),
                Category.builder().name("Room").type(CategoryType.ACCOMMODATION).icon("🛏️").build(),
                Category.builder().name("Hotel").type(CategoryType.ACCOMMODATION).icon("🏩").build(),
                Category.builder().name("Dormitory").type(CategoryType.ACCOMMODATION).icon("🛌").build(),
                Category.builder().name("Electronics").type(CategoryType.PRODUCT).icon("💻").build(),
                Category.builder().name("Mobile Phones").type(CategoryType.PRODUCT).icon("📱").build(),
                Category.builder().name("Furniture").type(CategoryType.PRODUCT).icon("🪑").build(),
                Category.builder().name("Books & Stationery").type(CategoryType.PRODUCT).icon("📚").build(),
                Category.builder().name("Home Appliances").type(CategoryType.PRODUCT).icon("🧺").build(),
                Category.builder().name("Vehicles").type(CategoryType.PRODUCT).icon("🏍️").build(),
                Category.builder().name("Sports & Fitness").type(CategoryType.PRODUCT).icon("🏏").build(),
                Category.builder().name("Home & Kitchen").type(CategoryType.PRODUCT).icon("🍳").build(),
                Category.builder().name("Fashion").type(CategoryType.PRODUCT).icon("👕").build(),
                Category.builder().name("Others").type(CategoryType.PRODUCT).icon("📦").build()
        );
        categoryRepository.saveAll(categories);
        log.info("Seeded {} categories", categories.size());
    }

    private void seedAdmin() {
        userRepository.findByEmail(adminEmail).ifPresentOrElse(
                existing -> log.info("Admin user already exists: {}", adminEmail),
                () -> {
                    User admin = User.builder()
                            .name(adminName)
                            .email(adminEmail)
                            .passwordHash(passwordEncoder.encode(adminPassword))
                            .phone("0000000000")
                            .role(Role.ADMIN)
                            .city("Dehradun")
                            .state("Uttarakhand")
                            .isActive(true)
                            .isVerified(true)
                            .build();
                    userRepository.save(admin);
                    log.info("Seeded admin user: {}", adminEmail);
                });
    }
}