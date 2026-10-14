package com.staymart.dto.response;

import com.staymart.entity.Review;
import com.staymart.entity.enums.ReviewItemType;

import java.time.LocalDateTime;

public record ReviewResponse(
        Long id,
        UserSummary reviewer,
        ReviewItemType itemType,
        Long itemId,
        Integer rating,
        String comment,
        LocalDateTime createdAt
) {
    public static ReviewResponse from(Review review) {
        return new ReviewResponse(
                review.getId(),
                UserSummary.from(review.getReviewer()),
                review.getItemType(),
                review.getItemId(),
                review.getRating(),
                review.getComment(),
                review.getCreatedAt()
        );
    }
}