package com.staymart.dto.request;

import com.staymart.entity.enums.GenderPreference;
import com.staymart.entity.enums.PropertyType;
import org.springframework.data.domain.Pageable;

import java.math.BigDecimal;

public record PropertySearchCriteria(
        PropertyType type,
        String city,
        String area,
        GenderPreference genderPreference,
        BigDecimal minPrice,
        BigDecimal maxPrice,
        String keyword,
        Boolean available,
        Pageable pageable
) {
}