package com.staymart.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;

public record LocationRequest(
        @NotBlank(message = "City is required")
        @Size(max = 100, message = "City must be at most 100 characters")
        String city,

        @Size(max = 100, message = "Area must be at most 100 characters")
        String area,

        @Size(max = 100, message = "State must be at most 100 characters")
        String state,

        @Size(max = 10, message = "Pincode must be at most 10 characters")
        String pincode,

        BigDecimal latitude,

        BigDecimal longitude
) {
}
