package com.staymart.dto.response;

import com.staymart.entity.Property;
import com.staymart.entity.enums.GenderPreference;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.entity.enums.PropertyType;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

public record PropertyResponse(
        Long id,
        String title,
        String description,
        PropertyType type,
        GenderPreference genderPreference,
        String address,
        String area,
        LocationResponse location,
        BigDecimal pricePerMonth,
        BigDecimal depositAmount,
        List<String> amenities,
        Integer totalRooms,
        Integer availableRooms,
        List<String> images,
        ModerationStatus status,
        Boolean isAvailable,
        UserSummary postedBy,
        LocalDateTime createdAt
) {
    public static PropertyResponse from(Property property) {
        return new PropertyResponse(
                property.getId(),
                property.getTitle(),
                property.getDescription(),
                property.getType(),
                property.getGenderPreference(),
                property.getAddress(),
                property.getArea(),
                LocationResponse.from(property.getLocation()),
                property.getPricePerMonth(),
                property.getDepositAmount(),
                property.getAmenities(),
                property.getTotalRooms(),
                property.getAvailableRooms(),
                property.getImages(),
                property.getStatus(),
                property.getIsAvailable(),
                UserSummary.from(property.getPostedBy()),
                property.getCreatedAt()
        );
    }
}