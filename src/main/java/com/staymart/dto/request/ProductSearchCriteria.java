package com.staymart.dto.request;

import com.staymart.entity.enums.ListingType;
import com.staymart.entity.enums.ProductCondition;
import org.springframework.data.domain.Pageable;

import java.math.BigDecimal;

public record ProductSearchCriteria(
        Long categoryId,
        ListingType listingType,
        ProductCondition condition,
        BigDecimal minPrice,
        BigDecimal maxPrice,
        String area,
        String city,
        String keyword,
        Boolean available,
        Pageable pageable
) {
}