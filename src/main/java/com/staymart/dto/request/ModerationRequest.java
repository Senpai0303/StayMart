package com.staymart.dto.request;

import com.staymart.entity.enums.ModerationStatus;
import jakarta.validation.constraints.NotNull;

public record ModerationRequest(
        @NotNull(message = "Status is required")
        ModerationStatus status
) {
}