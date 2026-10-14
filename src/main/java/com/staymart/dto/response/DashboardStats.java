package com.staymart.dto.response;

import com.staymart.entity.enums.BookingStatus;

public record DashboardStats(
        long totalUsers,
        long totalProperties,
        long approvedProperties,
        long pendingProperties,
        long totalProducts,
        long approvedProducts,
        long pendingProducts,
        long totalBookings,
        long pendingBookings,
        long totalOrders,
        long unreadChatCount
) {
}