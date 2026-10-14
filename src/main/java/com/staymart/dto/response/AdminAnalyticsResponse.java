package com.staymart.dto.response;

import java.util.List;

public record AdminAnalyticsResponse(
        long totalUsers,
        long totalProperties,
        long totalProducts,
        long totalBookings,
        long totalOrders,
        List<ChartDataPoint> monthlyListings,
        List<ChartDataPoint> monthlyRegistrations,
        List<ChartDataPoint> propertiesByType,
        List<ChartDataPoint> productsByCategory,
        List<ChartDataPoint> usersByCity
) {
}
