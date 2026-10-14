package com.staymart.dto.request;

import com.staymart.entity.enums.GenderPreference;
import com.staymart.entity.enums.PropertyType;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;
import java.util.List;

public record PropertyRequest(
        @NotBlank(message = "Title is required")
        @Size(max = 200, message = "Title must be at most 200 characters")
        String title,

        @Size(max = 5000, message = "Description must be at most 5000 characters")
        String description,

        @NotNull(message = "Property type is required")
        PropertyType type,

        GenderPreference genderPreference,

        @Size(max = 255, message = "Address must be at most 255 characters")
        String address,

        @Size(max = 100, message = "Area must be at most 100 characters")
        String area,

        Long locationId,

        @DecimalMin(value = "0.0", message = "Price per month must be positive")
        BigDecimal pricePerMonth,

        @DecimalMin(value = "0.0", message = "Deposit must be positive")
        BigDecimal depositAmount,

        List<String> amenities,

        @Min(value = 1, message = "Total rooms must be at least 1")
        Integer totalRooms,

        @Min(value = 0, message = "Available rooms cannot be negative")
        Integer availableRooms,

        List<String> images
) {
}