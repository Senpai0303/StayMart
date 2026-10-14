package com.staymart.dto.response;

import com.staymart.entity.Booking;
import com.staymart.entity.enums.BookingStatus;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

public record BookingResponse(
        Long id,
        UserSummary booker,
        PropertyResponse property,
        RoomResponse room,
        LocalDate checkIn,
        LocalDate checkOut,
        BigDecimal totalAmount,
        Integer months,
        BookingStatus status,
        String message,
        LocalDateTime createdAt
) {
    public static BookingResponse from(Booking booking) {
        return new BookingResponse(
                booking.getId(),
                UserSummary.from(booking.getBooker()),
                PropertyResponse.from(booking.getProperty()),
                RoomResponse.from(booking.getRoom()),
                booking.getCheckIn(),
                booking.getCheckOut(),
                booking.getTotalAmount(),
                booking.getMonths(),
                booking.getStatus(),
                booking.getMessage(),
                booking.getCreatedAt()
        );
    }
}