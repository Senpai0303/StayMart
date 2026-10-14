package com.staymart.dto.response;

import com.staymart.entity.enums.WishlistItemType;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record WishlistResponse(
        Long id,
        WishlistItemType itemType,
        Long itemId,
        String title,
        String image,
        BigDecimal price,
        LocalDateTime createdAt
) {
}