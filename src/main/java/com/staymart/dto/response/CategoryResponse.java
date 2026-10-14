package com.staymart.dto.response;

import com.staymart.entity.Category;
import com.staymart.entity.enums.CategoryType;

public record CategoryResponse(
        Long id,
        String name,
        CategoryType type,
        String icon,
        Long parentId
) {
    public static CategoryResponse from(Category category) {
        if (category == null) {
            return null;
        }
        return new CategoryResponse(
                category.getId(),
                category.getName(),
                category.getType(),
                category.getIcon(),
                category.getParentId()
        );
    }
}