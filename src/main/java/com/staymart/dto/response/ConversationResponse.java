package com.staymart.dto.response;

import java.time.LocalDateTime;

public record ConversationResponse(
        UserSummary partner,
        String lastMessage,
        LocalDateTime lastMessageAt,
        long unreadCount
) {
}