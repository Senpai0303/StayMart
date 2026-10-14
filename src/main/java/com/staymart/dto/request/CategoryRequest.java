package com.staymart.dto.request;

import com.staymart.entity.enums.CategoryType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record CategoryRequest(
        @NotBlank(message = "Category name is required")
        @Size(max = 100, message = "Category name must be at most 100 characters")
        String name,

        @NotNull(message = "Category type is required")
        CategoryType type,

        @Size(max = 50, message = "Icon must be at most 50 characters")
        String icon,

        Long parentId
) {
}
