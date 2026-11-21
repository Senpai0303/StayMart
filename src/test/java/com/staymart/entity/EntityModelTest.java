package com.staymart.entity;

import com.staymart.entity.enums.BookingStatus;
import com.staymart.entity.enums.OrderStatus;
import com.staymart.entity.enums.PropertyType;
import com.staymart.entity.enums.Role;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

public class EntityModelTest {

    @Test
    @DisplayName("User entity builder and defaults")
    void testUserEntity() {
        User user = User.builder()
                .name("Test User")
                .email("test@staymart.com")
                .passwordHash("hashed")
                .city("Dehradun")
                .role(Role.USER)
                .build();

        assertEquals("Test User", user.getName());
        assertEquals("test@staymart.com", user.getEmail());
        assertEquals("Dehradun", user.getCity());
        assertTrue(user.getIsActive());
        assertFalse(user.getIsVerified());
    }

    @Test
    @DisplayName("Booking entity months and status defaults")
    void testBookingDefaults() {
        Booking booking = Booking.builder()
                .checkIn(LocalDate.now())
                .checkOut(LocalDate.now().plusMonths(3))
                .totalAmount(BigDecimal.valueOf(15000))
                .build();

        assertEquals(1, booking.getMonths());
        assertEquals(BookingStatus.PENDING, booking.getStatus());
        assertEquals(BigDecimal.valueOf(15000), booking.getTotalAmount());
    }

    @Test
    @DisplayName("Order entity quantity and status defaults")
    void testOrderDefaults() {
        Order order = Order.builder()
                .amount(BigDecimal.valueOf(2500))
                .build();

        assertEquals(1, order.getQuantity());
        assertEquals(OrderStatus.PENDING, order.getStatus());
        assertEquals(BigDecimal.valueOf(2500), order.getAmount());
    }

    @Test
    @DisplayName("Property entity defaults")
    void testPropertyDefaults() {
        Property property = Property.builder()
                .title("Sunrise Boys PG")
                .type(PropertyType.PG)
                .pricePerMonth(BigDecimal.valueOf(6500))
                .build();

        assertEquals("Sunrise Boys PG", property.getTitle());
        assertEquals(PropertyType.PG, property.getType());
        assertEquals(1, property.getTotalRooms());
        assertEquals(1, property.getAvailableRooms());
    }
}
