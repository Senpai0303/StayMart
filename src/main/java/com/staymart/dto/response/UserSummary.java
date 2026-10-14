package com.staymart.dto.response;

import com.staymart.entity.User;

public record UserSummary(
        Long id,
        String name,
        String profilePic,
        String phone,
        String city,
        Boolean isVerified
) {
    public static UserSummary from(User user) {
        if (user == null) {
            return null;
        }
        return new UserSummary(
                user.getId(),
                user.getName(),
                user.getProfilePic(),
                user.getPhone(),
                user.getCity(),
                user.getIsVerified()
        );
    }
}