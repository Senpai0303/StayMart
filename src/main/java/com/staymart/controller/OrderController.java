package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.OrderRequest;
import com.staymart.dto.response.OrderResponse;
import com.staymart.entity.enums.OrderStatus;
import com.staymart.service.OrderService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/orders")
@Tag(name = "Orders", description = "Product buy/rent orders")
@SecurityRequirement(name = "bearerAuth")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @PostMapping
    @Operation(summary = "Place an order for a product")
    public ApiResponse<OrderResponse> create(@Valid @RequestBody OrderRequest request) {
        return ApiResponse.ok("Order placed", orderService.create(request));
    }

    @GetMapping("/mine")
    @Operation(summary = "List orders placed by me")
    public ApiResponse<PageResponse<OrderResponse>> getMyOrders(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(orderService.getMyOrders(pageable(page, size)));
    }

    @GetMapping("/sales")
    @Operation(summary = "List orders received on my products")
    public ApiResponse<PageResponse<OrderResponse>> getMySales(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(orderService.getMySales(pageable(page, size)));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get an order by id")
    public ApiResponse<OrderResponse> getById(@PathVariable Long id) {
        return ApiResponse.ok(orderService.getById(id));
    }

    @PatchMapping("/{id}/status")
    @Operation(summary = "Update order status (seller/admin)")
    public ApiResponse<OrderResponse> updateStatus(@PathVariable Long id,
                                                   @RequestParam OrderStatus status) {
        return ApiResponse.ok("Order status updated", orderService.updateStatus(id, status));
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 100), Sort.by(Sort.Direction.DESC, "createdAt"));
    }
}