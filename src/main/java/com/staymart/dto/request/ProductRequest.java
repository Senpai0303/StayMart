package com.staymart.dto.request;

import com.staymart.entity.enums.ListingType;
import com.staymart.entity.enums.ProductCondition;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;
import java.util.List;

public record ProductRequest(
        Long categoryId,

        @NotBlank(message = "Title is required")
        @Size(max = 200, message = "Title must be at most 200 characters")
        String title,

        @Size(max = 5000, message = "Description must be at most 5000 characters")
        String description,

        @NotNull(message = "Price is required")
        @DecimalMin(value = "0.0", message = "Price must be positive")
        BigDecimal price,

        ListingType listingType,

        ProductCondition condition,

        @Size(max = 100, message = "Brand must be at most 100 characters")
        String brand,

        Long locationId,

        @Size(max = 100, message = "Area must be at most 100 characters")
        String area,

        List<String> images
) {
}