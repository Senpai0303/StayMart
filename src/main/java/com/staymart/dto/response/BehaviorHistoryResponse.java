package com.staymart.dto.response;

import com.staymart.entity.UserBehavior;
import com.staymart.entity.enums.BehaviorAction;
import com.staymart.entity.enums.BehaviorItemType;

import java.time.LocalDateTime;

public record BehaviorHistoryResponse(
        Long id,
        BehaviorItemType itemType,
        Long itemId,
        BehaviorAction action,
        String searchQuery,
        String cityFilter,
        LocalDateTime timestamp
) {
    public static BehaviorHistoryResponse from(UserBehavior behavior) {
        return new BehaviorHistoryResponse(
                behavior.getId(),
                behavior.getItemType(),
                behavior.getItemId(),
                behavior.getAction(),
                behavior.getSearchQuery(),
                behavior.getCityFilter(),
                behavior.getTimestamp()
        );
    }
}