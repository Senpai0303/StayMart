package com.staymart.dto.request;

import jakarta.validation.constraints.Size;

public record UpdateProfileRequest(
        @Size(max = 100, message = "Name must be at most 100 characters")
        String name,

        @Size(max = 15, message = "Phone must be at most 15 characters")
        String phone,

        @Size(max = 255, message = "Profile picture URL is too long")
        String profilePic,

        @Size(max = 100, message = "City must be at most 100 characters")
        String city,

        @Size(max = 100, message = "State must be at most 100 characters")
        String state,

        @Size(max = 2000, message = "Bio must be at most 2000 characters")
        String bio
) {
}