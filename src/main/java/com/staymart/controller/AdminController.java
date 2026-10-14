package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.ModerationRequest;
import com.staymart.dto.response.AdminAnalyticsResponse;
import com.staymart.dto.response.DashboardStats;
import com.staymart.dto.response.PropertyResponse;
import com.staymart.dto.response.ProductResponse;
import com.staymart.dto.response.UserResponse;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.service.AdminService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/admin")
@Tag(name = "Admin", description = "Admin moderation and platform management")
@SecurityRequirement(name = "bearerAuth")
public class AdminController {

    private final AdminService adminService;

    public AdminController(AdminService adminService) {
        this.adminService = adminService;
    }

    @GetMapping("/stats")
    @Operation(summary = "Platform dashboard statistics")
    public ApiResponse<DashboardStats> stats() {
        return ApiResponse.ok(adminService.stats());
    }

    @GetMapping("/analytics")
    @Operation(summary = "Platform analytics for charts")
    public ApiResponse<AdminAnalyticsResponse> analytics() {
        return ApiResponse.ok(adminService.analytics());
    }

    @GetMapping("/users")
    @Operation(summary = "List all users")
    public ApiResponse<PageResponse<UserResponse>> listUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(adminService.listUsers(pageable(page, size)));
    }

    @PatchMapping("/users/{id}/status")
    @Operation(summary = "Activate or deactivate a user")
    public ApiResponse<UserResponse> setUserActive(@PathVariable Long id,
                                                   @RequestParam boolean active) {
        return ApiResponse.ok(active ? "User activated" : "User deactivated",
                adminService.setUserActive(id, active));
    }

    @DeleteMapping("/users/{id}")
    @Operation(summary = "Delete a user (only when they have no listings)")
    public ApiResponse<Void> deleteUser(@PathVariable Long id) {
        adminService.deleteUser(id);
        return ApiResponse.ok("User deleted", null);
    }

    @GetMapping("/properties")
    @Operation(summary = "List properties, optionally filtered by moderation status")
    public ApiResponse<PageResponse<PropertyResponse>> listProperties(
            @RequestParam(required = false) ModerationStatus status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(adminService.listProperties(status, pageable(page, size)));
    }

    @PatchMapping("/properties/{id}/status")
    @Operation(summary = "Approve or reject a property listing")
    public ApiResponse<PropertyResponse> moderateProperty(@PathVariable Long id,
                                                          @Valid @RequestBody ModerationRequest request) {
        return ApiResponse.ok("Property status updated", adminService.moderateProperty(id, request));
    }

    @GetMapping("/products")
    @Operation(summary = "List products, optionally filtered by moderation status")
    public ApiResponse<PageResponse<ProductResponse>> listProducts(
            @RequestParam(required = false) ModerationStatus status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(adminService.listProducts(status, pageable(page, size)));
    }

    @PatchMapping("/products/{id}/status")
    @Operation(summary = "Approve or reject a product listing")
    public ApiResponse<ProductResponse> moderateProduct(@PathVariable Long id,
                                                        @Valid @RequestBody ModerationRequest request) {
        return ApiResponse.ok("Product status updated", adminService.moderateProduct(id, request));
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 100), Sort.by(Sort.Direction.DESC, "createdAt"));
    }
}