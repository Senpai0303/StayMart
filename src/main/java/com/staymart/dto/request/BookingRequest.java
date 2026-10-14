package com.staymart.dto.request;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;

public record BookingRequest(
        @NotNull(message = "Property id is required")
        Long propertyId,

        Long roomId,

        @NotNull(message = "Check-in date is required")
        LocalDate checkIn,

        LocalDate checkOut,

        @Min(value = 1, message = "Months must be at least 1")
        Integer months,

        @jakarta.validation.constraints.Size(max = 2000, message = "Message must be at most 2000 characters")
        String message
) {
}