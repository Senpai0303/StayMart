package com.staymart.dto.response;

import com.staymart.entity.User;
import com.staymart.entity.enums.Role;

import java.time.LocalDateTime;

public record UserResponse(
        Long id,
        String name,
        String email,
        String phone,
        Role role,
        String profilePic,
        String city,
        String state,
        String bio,
        Boolean isActive,
        Boolean isVerified,
        LocalDateTime createdAt
) {
    public static UserResponse from(User user) {
        return new UserResponse(
                user.getId(),
                user.getName(),
                user.getEmail(),
                user.getPhone(),
                user.getRole(),
                user.getProfilePic(),
                user.getCity(),
                user.getState(),
                user.getBio(),
                user.getIsActive(),
                user.getIsVerified(),
                user.getCreatedAt()
        );
    }
}