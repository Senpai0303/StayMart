package com.staymart.dto.response;

public record ReviewSummaryResponse(
        double averageRating,
        long count
) {
}