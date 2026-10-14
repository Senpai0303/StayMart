package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.OrderRequest;
import com.staymart.dto.response.OrderResponse;
import com.staymart.entity.Order;
import com.staymart.entity.Product;
import com.staymart.entity.User;
import com.staymart.entity.enums.BehaviorAction;
import com.staymart.entity.enums.BehaviorItemType;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.entity.enums.OrderStatus;
import com.staymart.entity.enums.OrderType;
import com.staymart.exception.AccessForbiddenException;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.OrderRepository;
import com.staymart.util.SecurityUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

@Service
public class OrderService {

    private final OrderRepository orderRepository;
    private final ProductService productService;
    private final BehaviorService behaviorService;

    public OrderService(OrderRepository orderRepository,
                        ProductService productService,
                        BehaviorService behaviorService) {
        this.orderRepository = orderRepository;
        this.productService = productService;
        this.behaviorService = behaviorService;
    }

    @Transactional
    public OrderResponse create(OrderRequest request) {
        User buyer = SecurityUtils.currentUser();
        Product product = productService.findProduct(request.productId());

        if (product.getStatus() != ModerationStatus.APPROVED) {
            throw new BadRequestException("This product is not available yet");
        }
        if (buyer.getId().equals(product.getPostedBy().getId())) {
            throw new BadRequestException("You cannot order your own product");
        }
        if (!Boolean.TRUE.equals(product.getIsAvailable())) {
            throw new BadRequestException("This product is currently unavailable");
        }

        OrderType orderType = request.orderType() == null ? OrderType.BUY : request.orderType();
        if (orderType == OrderType.RENT
                && (request.rentStart() == null || request.rentEnd() == null)) {
            throw new BadRequestException("Rent start and end dates are required for rental orders");
        }
        if (request.rentStart() != null && request.rentEnd() != null
                && !request.rentEnd().isAfter(request.rentStart())) {
            throw new BadRequestException("Rent end date must be after rent start date");
        }
        if (orderType == OrderType.BUY && product.getListingType() == com.staymart.entity.enums.ListingType.RENT) {
            throw new BadRequestException("This product is available for rent only");
        }
        if (orderType == OrderType.RENT && product.getListingType() == com.staymart.entity.enums.ListingType.SELL) {
            throw new BadRequestException("This product is available for purchase only");
        }

        int quantity = request.quantity() == null ? 1 : request.quantity();
        BigDecimal amount = product.getPrice() == null
                ? BigDecimal.ZERO
                : product.getPrice().multiply(BigDecimal.valueOf(quantity));

        Order order = Order.builder()
                .buyer(buyer)
                .product(product)
                .seller(product.getPostedBy())
                .quantity(quantity)
                .amount(amount)
                .orderType(orderType)
                .rentStart(request.rentStart())
                .rentEnd(request.rentEnd())
                .status(OrderStatus.PENDING)
                .message(request.message())
                .build();

        Order saved = orderRepository.save(order);
        behaviorService.record(buyer.getId(), BehaviorItemType.PRODUCT, product.getId(),
                BehaviorAction.ORDER, null, product.getArea());
        return OrderResponse.from(saved);
    }

    @Transactional
    public OrderResponse updateStatus(Long orderId, OrderStatus status) {
        Order order = findOrder(orderId);
        if (!isSellerOrAdmin(order) && !isBuyer(order)) {
            throw new AccessForbiddenException("You can only update your own orders");
        }
        if (status == OrderStatus.PENDING) {
            throw new BadRequestException("Invalid status change");
        }

        order.setStatus(status);

        if (status == OrderStatus.COMPLETED) {
            Product product = order.getProduct();
            product.setIsAvailable(false);
        }

        return OrderResponse.from(orderRepository.save(order));
    }

    @Transactional(readOnly = true)
    public PageResponse<OrderResponse> getMyOrders(Pageable pageable) {
        Page<Order> page = orderRepository.findByBuyerId(SecurityUtils.currentUserId(), pageable);
        return PageResponse.of(page, OrderResponse::from);
    }

    @Transactional(readOnly = true)
    public PageResponse<OrderResponse> getMySales(Pageable pageable) {
        Page<Order> page = orderRepository.findBySellerId(SecurityUtils.currentUserId(), pageable);
        return PageResponse.of(page, OrderResponse::from);
    }

    @Transactional(readOnly = true)
    public OrderResponse getById(Long orderId) {
        Order order = findOrder(orderId);
        if (!isSellerOrAdmin(order) && !isBuyer(order)) {
            throw new AccessForbiddenException("You can only view your own orders");
        }
        return OrderResponse.from(order);
    }

    @Transactional(readOnly = true)
    public Order findOrder(Long orderId) {
        return orderRepository.findById(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order not found with id: " + orderId));
    }

    private boolean isSellerOrAdmin(Order order) {
        User current = SecurityUtils.currentUser();
        return current.getRole() == com.staymart.entity.enums.Role.ADMIN
                || current.getId().equals(order.getSeller().getId());
    }

    private boolean isBuyer(Order order) {
        return SecurityUtils.currentUserId().equals(order.getBuyer().getId());
    }
}