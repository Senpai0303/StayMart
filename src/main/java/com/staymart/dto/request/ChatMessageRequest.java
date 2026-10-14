package com.staymart.dto.request;

import com.staymart.entity.enums.ChatListingType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record ChatMessageRequest(
        @NotNull(message = "Receiver id is required")
        Long receiverId,

        ChatListingType listingType,

        Long listingId,

        @NotBlank(message = "Message cannot be empty")
        @Size(max = 2000, message = "Message must be at most 2000 characters")
        String message
) {
}