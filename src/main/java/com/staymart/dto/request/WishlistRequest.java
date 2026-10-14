package com.staymart.dto.request;

import com.staymart.entity.enums.WishlistItemType;
import jakarta.validation.constraints.NotNull;

public record WishlistRequest(
        @NotNull(message = "Item type is required")
        WishlistItemType itemType,

        @NotNull(message = "Item id is required")
        Long itemId
) {
}