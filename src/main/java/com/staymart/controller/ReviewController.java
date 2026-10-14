package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.ReviewRequest;
import com.staymart.dto.response.ReviewResponse;
import com.staymart.dto.response.ReviewSummaryResponse;
import com.staymart.entity.enums.ReviewItemType;
import com.staymart.service.ReviewService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/reviews")
@Tag(name = "Reviews", description = "Ratings and reviews for properties, products and users")
public class ReviewController {

    private final ReviewService reviewService;

    public ReviewController(ReviewService reviewService) {
        this.reviewService = reviewService;
    }

    @GetMapping
    @Operation(summary = "List reviews for an item")
    public ApiResponse<PageResponse<ReviewResponse>> list(@RequestParam ReviewItemType itemType,
                                                          @RequestParam Long itemId,
                                                          @RequestParam(defaultValue = "0") int page,
                                                          @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(reviewService.listByItem(itemType, itemId, pageable(page, size)));
    }

    @GetMapping("/summary")
    @Operation(summary = "Average rating and review count for an item")
    public ApiResponse<ReviewSummaryResponse> summary(@RequestParam ReviewItemType itemType,
                                                      @RequestParam Long itemId) {
        return ApiResponse.ok(new ReviewSummaryResponse(
                reviewService.averageRating(itemType, itemId),
                reviewService.count(itemType, itemId)));
    }

    @PostMapping
    @Operation(summary = "Submit a review", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<ReviewResponse> add(@Valid @RequestBody ReviewRequest request) {
        return ApiResponse.ok("Review submitted", reviewService.add(request));
    }

    @GetMapping("/mine")
    @Operation(summary = "List reviews written by me", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<PageResponse<ReviewResponse>> mine(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(reviewService.listMine(pageable(page, size)));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete one of my reviews", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<Void> delete(@PathVariable Long id) {
        reviewService.delete(id);
        return ApiResponse.ok("Review deleted", null);
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 100), Sort.by(Sort.Direction.DESC, "createdAt"));
    }
}