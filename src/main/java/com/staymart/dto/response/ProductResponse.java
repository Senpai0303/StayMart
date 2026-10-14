package com.staymart.dto.response;

import com.staymart.entity.Product;
import com.staymart.entity.enums.ListingType;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.entity.enums.ProductCondition;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

public record ProductResponse(
        Long id,
        String title,
        String description,
        CategoryResponse category,
        BigDecimal price,
        ListingType listingType,
        ProductCondition condition,
        String brand,
        String area,
        LocationResponse location,
        List<String> images,
        ModerationStatus status,
        Boolean isAvailable,
        Integer viewsCount,
        UserSummary postedBy,
        LocalDateTime createdAt
) {
    public static ProductResponse from(Product product) {
        return new ProductResponse(
                product.getId(),
                product.getTitle(),
                product.getDescription(),
                CategoryResponse.from(product.getCategory()),
                product.getPrice(),
                product.getListingType(),
                product.getCondition(),
                product.getBrand(),
                product.getArea(),
                LocationResponse.from(product.getLocation()),
                product.getImages(),
                product.getStatus(),
                product.getIsAvailable(),
                product.getViewsCount(),
                UserSummary.from(product.getPostedBy()),
                product.getCreatedAt()
        );
    }
}