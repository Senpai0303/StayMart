package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.BehaviorRequest;
import com.staymart.dto.response.BehaviorHistoryResponse;
import com.staymart.dto.response.RecommendationResponse;
import com.staymart.service.BehaviorService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/behaviors")
@Tag(name = "Behaviors", description = "User behavior tracking and recommendations")
@SecurityRequirement(name = "bearerAuth")
public class BehaviorController {

    private final BehaviorService behaviorService;

    public BehaviorController(BehaviorService behaviorService) {
        this.behaviorService = behaviorService;
    }

    @PostMapping
    @Operation(summary = "Record a behavior event (VIEW/SEARCH/WISHLIST/BOOK/ORDER/CONTACT)")
    public ApiResponse<Void> record(@Valid @RequestBody BehaviorRequest request) {
        behaviorService.recordExplicit(request);
        return ApiResponse.ok("Behavior recorded", null);
    }

    @GetMapping("/history")
    @Operation(summary = "My behavior history")
    public ApiResponse<PageResponse<BehaviorHistoryResponse>> history(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size) {
        return ApiResponse.ok(behaviorService.getHistory(pageable(page, size)));
    }

    @GetMapping("/recommendations")
    @Operation(summary = "Personalized recommendations based on my behavior")
    public ApiResponse<RecommendationResponse> recommendations(
            @RequestParam(defaultValue = "10") int limit) {
        return ApiResponse.ok(behaviorService.recommendations(limit));
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 100), Sort.by(Sort.Direction.DESC, "timestamp"));
    }
}