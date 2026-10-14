package com.staymart.dto.request;

import com.staymart.entity.enums.BehaviorAction;
import com.staymart.entity.enums.BehaviorItemType;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record BehaviorRequest(
        @NotNull(message = "Item type is required")
        BehaviorItemType itemType,

        @NotNull(message = "Item id is required")
        Long itemId,

        @NotNull(message = "Action is required")
        BehaviorAction action,

        @Size(max = 255, message = "Search query must be at most 255 characters")
        String searchQuery,

        @Size(max = 100, message = "City filter must be at most 100 characters")
        String cityFilter
) {
}