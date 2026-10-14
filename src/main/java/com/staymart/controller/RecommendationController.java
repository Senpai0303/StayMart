package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.dto.response.ProductResponse;
import com.staymart.dto.response.PropertyResponse;
import com.staymart.service.RecommendationService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/recommendations")
@Tag(name = "Recommendations", description = "Personalized and trending recommendations backed by the ML service")
public class RecommendationController {

    private final RecommendationService recommendationService;

    public RecommendationController(RecommendationService recommendationService) {
        this.recommendationService = recommendationService;
    }

    @GetMapping("/{userId}")
    @Operation(summary = "Personalized property recommendations for a user")
    public ApiResponse<List<PropertyResponse>> forUser(@PathVariable Long userId,
                                                       @RequestParam(defaultValue = "10") int limit,
                                                       @RequestParam(required = false) String city) {
        return ApiResponse.ok(recommendationService.recommendedProperties(userId, city, limit));
    }

    @GetMapping("/properties")
    @Operation(summary = "Personalized property recommendations (current user, optional userId)")
    public ApiResponse<List<PropertyResponse>> recommendedProperties(
            @RequestParam(required = false) Long userId,
            @RequestParam(required = false) String city,
            @RequestParam(defaultValue = "8") int limit) {
        return ApiResponse.ok(recommendationService.recommendedProperties(userId, city, limit));
    }

    @GetMapping("/properties/trending")
    @Operation(summary = "Trending properties")
    public ApiResponse<List<PropertyResponse>> trendingProperties(
            @RequestParam(required = false) String city,
            @RequestParam(defaultValue = "8") int limit) {
        return ApiResponse.ok(recommendationService.trendingProperties(city, limit));
    }

    @GetMapping("/properties/{propertyId}/similar")
    @Operation(summary = "Properties similar to the given property")
    public ApiResponse<List<PropertyResponse>> similarProperties(@PathVariable Long propertyId,
                                                                 @RequestParam(defaultValue = "4") int limit) {
        return ApiResponse.ok(recommendationService.similarProperties(propertyId, limit));
    }

    @GetMapping("/products")
    @Operation(summary = "Personalized product recommendations (current user, optional userId)")
    public ApiResponse<List<ProductResponse>> recommendedProducts(
            @RequestParam(required = false) Long userId,
            @RequestParam(required = false) String city,
            @RequestParam(defaultValue = "8") int limit) {
        return ApiResponse.ok(recommendationService.recommendedProducts(userId, city, limit));
    }

    @GetMapping("/products/top-rated")
    @Operation(summary = "Top-rated products")
    public ApiResponse<List<ProductResponse>> topRatedProducts(
            @RequestParam(required = false) String city,
            @RequestParam(defaultValue = "8") int limit) {
        return ApiResponse.ok(recommendationService.trendingProducts(city, limit));
    }
}
