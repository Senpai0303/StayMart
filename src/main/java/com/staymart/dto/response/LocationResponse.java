package com.staymart.dto.response;

import com.staymart.entity.Location;

import java.math.BigDecimal;

public record LocationResponse(
        Long id,
        String city,
        String area,
        String state,
        String pincode,
        BigDecimal latitude,
        BigDecimal longitude
) {
    public static LocationResponse from(Location location) {
        if (location == null) {
            return null;
        }
        return new LocationResponse(
                location.getId(),
                location.getCity(),
                location.getArea(),
                location.getState(),
                location.getPincode(),
                location.getLatitude(),
                location.getLongitude()
        );
    }
}