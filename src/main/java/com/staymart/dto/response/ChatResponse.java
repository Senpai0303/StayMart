package com.staymart.dto.response;

import com.staymart.entity.Chat;
import com.staymart.entity.enums.ChatListingType;

import java.time.LocalDateTime;

public record ChatResponse(
        Long id,
        UserSummary sender,
        UserSummary receiver,
        ChatListingType listingType,
        Long listingId,
        String message,
        LocalDateTime timestamp,
        Boolean isRead
) {
    public static ChatResponse from(Chat chat) {
        return new ChatResponse(
                chat.getId(),
                UserSummary.from(chat.getSender()),
                UserSummary.from(chat.getReceiver()),
                chat.getListingType(),
                chat.getListingId(),
                chat.getMessage(),
                chat.getTimestamp(),
                chat.getIsRead()
        );
    }
}