package com.staymart.dto.response;

import com.staymart.entity.User;

public record AuthResponse(
        String token,
        String tokenType,
        long expiresIn,
        UserResponse user
) {
    public static AuthResponse of(String token, long expiresIn, User user) {
        return new AuthResponse(token, "Bearer", expiresIn, UserResponse.from(user));
    }
}