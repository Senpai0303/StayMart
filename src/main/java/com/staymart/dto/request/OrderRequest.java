package com.staymart.dto.request;

import com.staymart.entity.enums.OrderType;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.LocalDate;

public record OrderRequest(
        @NotNull(message = "Product id is required")
        Long productId,

        @Min(value = 1, message = "Quantity must be at least 1")
        Integer quantity,

        OrderType orderType,

        LocalDate rentStart,

        LocalDate rentEnd,

        @Size(max = 2000, message = "Message must be at most 2000 characters")
        String message
) {
}