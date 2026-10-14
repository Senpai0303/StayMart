package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.ChangePasswordRequest;
import com.staymart.dto.request.UpdateProfileRequest;
import com.staymart.dto.response.PropertyResponse;
import com.staymart.dto.response.ProductResponse;
import com.staymart.dto.response.UserResponse;
import com.staymart.dto.response.UserSummary;
import com.staymart.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/users")
@Tag(name = "Users", description = "User profile and listing management")
@SecurityRequirement(name = "bearerAuth")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/me")
    @Operation(summary = "Get my profile")
    public ApiResponse<UserResponse> getMyProfile() {
        return ApiResponse.ok(userService.getMyProfile());
    }

    @PutMapping("/me")
    @Operation(summary = "Update my profile")
    public ApiResponse<UserResponse> updateMyProfile(@Valid @RequestBody UpdateProfileRequest request) {
        return ApiResponse.ok("Profile updated", userService.updateMyProfile(request));
    }

    @PutMapping("/me/password")
    @Operation(summary = "Change my password")
    public ApiResponse<Void> changePassword(@Valid @RequestBody ChangePasswordRequest request) {
        userService.changePassword(request);
        return ApiResponse.ok("Password changed successfully", null);
    }

    @GetMapping("/me/properties")
    @Operation(summary = "List my property listings")
    public ApiResponse<PageResponse<PropertyResponse>> getMyProperties(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(userService.getMyProperties(pageable(page, size)));
    }

    @GetMapping("/me/products")
    @Operation(summary = "List my product listings")
    public ApiResponse<PageResponse<ProductResponse>> getMyProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(userService.getMyProducts(pageable(page, size)));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get a public profile summary")
    public ApiResponse<UserSummary> getUserSummary(@PathVariable Long id) {
        return ApiResponse.ok(userService.getUserSummary(id));
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 100), Sort.by(Sort.Direction.DESC, "createdAt"));
    }
}