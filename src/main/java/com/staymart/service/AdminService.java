package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.ModerationRequest;
import com.staymart.dto.response.AdminAnalyticsResponse;
import com.staymart.dto.response.ChartDataPoint;
import com.staymart.dto.response.DashboardStats;
import com.staymart.dto.response.PropertyResponse;
import com.staymart.dto.response.ProductResponse;
import com.staymart.dto.response.UserResponse;
import com.staymart.entity.Property;
import com.staymart.entity.Product;
import com.staymart.entity.User;
import com.staymart.entity.enums.BookingStatus;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.entity.enums.Role;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.BookingRepository;
import com.staymart.repository.ChatRepository;
import com.staymart.repository.OrderRepository;
import com.staymart.repository.ProductRepository;
import com.staymart.repository.PropertyRepository;
import com.staymart.repository.UserRepository;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class AdminService {

    private final UserRepository userRepository;
    private final PropertyRepository propertyRepository;
    private final ProductRepository productRepository;
    private final BookingRepository bookingRepository;
    private final OrderRepository orderRepository;
    private final ChatRepository chatRepository;

    public AdminService(UserRepository userRepository,
                        PropertyRepository propertyRepository,
                        ProductRepository productRepository,
                        BookingRepository bookingRepository,
                        OrderRepository orderRepository,
                        ChatRepository chatRepository) {
        this.userRepository = userRepository;
        this.propertyRepository = propertyRepository;
        this.productRepository = productRepository;
        this.bookingRepository = bookingRepository;
        this.orderRepository = orderRepository;
        this.chatRepository = chatRepository;
    }

    @Transactional(readOnly = true)
    public DashboardStats stats() {
        return new DashboardStats(
                userRepository.count(),
                propertyRepository.count(),
                propertyRepository.countByStatus(ModerationStatus.APPROVED),
                propertyRepository.countByStatus(ModerationStatus.PENDING),
                productRepository.count(),
                productRepository.countByStatus(ModerationStatus.APPROVED),
                productRepository.countByStatus(ModerationStatus.PENDING),
                bookingRepository.count(),
                bookingRepository.countByStatus(BookingStatus.PENDING),
                orderRepository.count(),
                chatRepository.countByIsReadFalse()
        );
    }

    @Transactional(readOnly = true)
    public PageResponse<UserResponse> listUsers(Pageable pageable) {
        Page<User> page = userRepository.findAll(pageable);
        return PageResponse.of(page, UserResponse::from);
    }

    @Transactional(readOnly = true)
    public PageResponse<UserResponse> listAdmins(Pageable pageable) {
        Page<User> page = userRepository.findByRole(Role.ADMIN, pageable);
        return PageResponse.of(page, UserResponse::from);
    }

    @Transactional
    public UserResponse setUserActive(Long userId, boolean active) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));
        if (user.getRole() == Role.ADMIN) {
            throw new BadRequestException("Admin accounts cannot be deactivated");
        }
        user.setIsActive(active);
        return UserResponse.from(userRepository.save(user));
    }

    @Transactional
    public void deleteUser(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));
        if (user.getRole() == Role.ADMIN) {
            throw new BadRequestException("Admin accounts cannot be deleted");
        }
        if (propertyRepository.countByPostedById(userId) > 0 || productRepository.countByPostedById(userId) > 0) {
            throw new BadRequestException("This user has listings. Deactivate the account instead of deleting it.");
        }
        try {
            userRepository.delete(user);
        } catch (DataIntegrityViolationException ex) {
            throw new BadRequestException("This user has related activity and cannot be deleted. Deactivate the account instead.");
        }
    }

    @Transactional(readOnly = true)
    public AdminAnalyticsResponse analytics() {
        LocalDate firstOfThisMonth = LocalDate.now().withDayOfMonth(1);
        LocalDateTime since = firstOfThisMonth.minusMonths(5).atStartOfDay();

        List<ChartDataPoint> monthlyListings = monthSeries(firstOfThisMonth);
        accumulate(monthlyListings, propertyRepository.countCreatedByMonthSince(since), firstOfThisMonth);
        accumulate(monthlyListings, productRepository.countCreatedByMonthSince(since), firstOfThisMonth);

        List<ChartDataPoint> monthlyRegistrations = monthSeries(firstOfThisMonth);
        accumulate(monthlyRegistrations, userRepository.countCreatedByMonthSince(since), firstOfThisMonth);

        return new AdminAnalyticsResponse(
                userRepository.count(),
                propertyRepository.count(),
                productRepository.count(),
                bookingRepository.count(),
                orderRepository.count(),
                monthlyListings,
                monthlyRegistrations,
                toStringPoints(propertyRepository.countGroupByType()),
                toStringPoints(productRepository.countGroupByCategory()),
                toStringPoints(userRepository.countGroupByCity())
        );
    }

    private List<ChartDataPoint> monthSeries(LocalDate firstOfThisMonth) {
        List<ChartDataPoint> points = new ArrayList<>();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MMM yy");
        for (int i = 5; i >= 0; i--) {
            points.add(new ChartDataPoint(firstOfThisMonth.minusMonths(i).format(formatter), 0L));
        }
        return points;
    }

    private void accumulate(List<ChartDataPoint> series, List<Object[]> rows, LocalDate firstOfThisMonth) {
        Map<String, Long> counts = new HashMap<>();
        for (Object[] row : rows) {
            String key = ((Number) row[0]).intValue() + "-" + ((Number) row[1]).intValue();
            counts.merge(key, ((Number) row[2]).longValue(), Long::sum);
        }
        for (int i = 0; i < series.size(); i++) {
            LocalDate month = firstOfThisMonth.minusMonths(5 - i);
            long value = counts.getOrDefault(month.getYear() + "-" + month.getMonthValue(), 0L);
            series.set(i, new ChartDataPoint(series.get(i).label(), value));
        }
    }

    private List<ChartDataPoint> toStringPoints(List<Object[]> rows) {
        List<ChartDataPoint> points = new ArrayList<>();
        for (Object[] row : rows) {
            String label = row[0] == null ? "Unknown" : String.valueOf(row[0]);
            points.add(new ChartDataPoint(label, ((Number) row[1]).longValue()));
        }
        return points;
    }

    @Transactional(readOnly = true)
    public PageResponse<PropertyResponse> listProperties(ModerationStatus status, Pageable pageable) {
        Page<Property> page = status == null
                ? propertyRepository.findAll(pageable)
                : propertyRepository.findByStatus(status, pageable);
        return PageResponse.of(page, PropertyResponse::from);
    }

    @Transactional
    public PropertyResponse moderateProperty(Long id, ModerationRequest request) {
        Property property = propertyRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Property not found with id: " + id));
        if (property.getStatus() == request.status()) {
            return PropertyResponse.from(property);
        }
        property.setStatus(request.status());
        return PropertyResponse.from(propertyRepository.save(property));
    }

    @Transactional(readOnly = true)
    public PageResponse<ProductResponse> listProducts(ModerationStatus status, Pageable pageable) {
        Page<Product> page = status == null
                ? productRepository.findAll(pageable)
                : productRepository.findByStatus(status, pageable);
        return PageResponse.of(page, ProductResponse::from);
    }

    @Transactional
    public ProductResponse moderateProduct(Long id, ModerationRequest request) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
        if (product.getStatus() == request.status()) {
            return ProductResponse.from(product);
        }
        product.setStatus(request.status());
        return ProductResponse.from(productRepository.save(product));
    }
}