package com.staymart.dto.request;

import com.staymart.entity.enums.RoomType;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;
import java.util.List;

public record RoomRequest(
        @Size(max = 20, message = "Room number must be at most 20 characters")
        String roomNumber,

        @NotNull(message = "Room type is required")
        RoomType type,

        @DecimalMin(value = "0.0", message = "Price must be positive")
        BigDecimal price,

        @Min(value = 1, message = "Capacity must be at least 1")
        Integer capacity,

        @Min(value = 0, message = "Floor number cannot be negative")
        Integer floorNumber,

        Boolean isAvailable,

        List<String> images
) {
}