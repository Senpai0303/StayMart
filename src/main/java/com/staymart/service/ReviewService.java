package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.ReviewRequest;
import com.staymart.dto.response.ReviewResponse;
import com.staymart.entity.Review;
import com.staymart.entity.User;
import com.staymart.entity.enums.ReviewItemType;
import com.staymart.entity.enums.Role;
import com.staymart.exception.AccessForbiddenException;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.ReviewRepository;
import com.staymart.util.SecurityUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ReviewService {

    private final ReviewRepository reviewRepository;

    public ReviewService(ReviewRepository reviewRepository) {
        this.reviewRepository = reviewRepository;
    }

    @Transactional
    public ReviewResponse add(ReviewRequest request) {
        User reviewer = SecurityUtils.currentUser();

        boolean duplicate = reviewRepository.existsByReviewerIdAndItemTypeAndItemId(
                reviewer.getId(), request.itemType(), request.itemId());
        if (duplicate) {
            throw new BadRequestException("You have already reviewed this item");
        }

        Review review = Review.builder()
                .reviewer(reviewer)
                .itemType(request.itemType())
                .itemId(request.itemId())
                .rating(request.rating())
                .comment(request.comment())
                .build();

        return ReviewResponse.from(reviewRepository.save(review));
    }

    @Transactional(readOnly = true)
    public PageResponse<ReviewResponse> listByItem(ReviewItemType itemType, Long itemId, Pageable pageable) {
        Page<Review> page = reviewRepository.findByItemTypeAndItemId(itemType, itemId, pageable);
        return PageResponse.of(page, ReviewResponse::from);
    }

    @Transactional(readOnly = true)
    public PageResponse<ReviewResponse> listMine(Pageable pageable) {
        Page<Review> page = reviewRepository.findByReviewerId(SecurityUtils.currentUserId(), pageable);
        return PageResponse.of(page, ReviewResponse::from);
    }

    @Transactional
    public void delete(Long reviewId) {
        Review review = reviewRepository.findById(reviewId)
                .orElseThrow(() -> new ResourceNotFoundException("Review not found with id: " + reviewId));
        User current = SecurityUtils.currentUser();
        if (!current.getId().equals(review.getReviewer().getId()) && current.getRole() != Role.ADMIN) {
            throw new AccessForbiddenException("You can only delete your own reviews");
        }
        reviewRepository.delete(review);
    }

    @Transactional(readOnly = true)
    public double averageRating(ReviewItemType itemType, Long itemId) {
        Double avg = reviewRepository.averageRating(itemType, itemId);
        return avg == null ? 0.0 : Math.round(avg * 10.0) / 10.0;
    }

    @Transactional(readOnly = true)
    public long count(ReviewItemType itemType, Long itemId) {
        return reviewRepository.countByItem(itemType, itemId);
    }
}