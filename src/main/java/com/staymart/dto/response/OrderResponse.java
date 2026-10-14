package com.staymart.dto.response;

import com.staymart.entity.Order;
import com.staymart.entity.enums.OrderStatus;
import com.staymart.entity.enums.OrderType;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

public record OrderResponse(
        Long id,
        UserSummary buyer,
        UserSummary seller,
        ProductResponse product,
        Integer quantity,
        BigDecimal amount,
        OrderType orderType,
        LocalDate rentStart,
        LocalDate rentEnd,
        OrderStatus status,
        String message,
        LocalDateTime createdAt
) {
    public static OrderResponse from(Order order) {
        return new OrderResponse(
                order.getId(),
                UserSummary.from(order.getBuyer()),
                UserSummary.from(order.getSeller()),
                ProductResponse.from(order.getProduct()),
                order.getQuantity(),
                order.getAmount(),
                order.getOrderType(),
                order.getRentStart(),
                order.getRentEnd(),
                order.getStatus(),
                order.getMessage(),
                order.getCreatedAt()
        );
    }
}