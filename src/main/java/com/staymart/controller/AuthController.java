package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.dto.request.LoginRequest;
import com.staymart.dto.request.RegisterRequest;
import com.staymart.dto.response.AuthResponse;
import com.staymart.dto.response.UserResponse;
import com.staymart.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
@Tag(name = "Auth", description = "Register, login and current user")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    @Operation(summary = "Register a new user")
    public ApiResponse<AuthResponse> register(@Valid @RequestBody RegisterRequest request) {
        return ApiResponse.ok("Registration successful", authService.register(request));
    }

    @PostMapping("/login")
    @Operation(summary = "Login and get a JWT token")
    public ApiResponse<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return ApiResponse.ok("Login successful", authService.login(request));
    }

    @GetMapping("/me")
    @Operation(summary = "Get the currently logged-in user", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<UserResponse> me() {
        return ApiResponse.ok(authService.me());
    }
}