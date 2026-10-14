package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.WishlistRequest;
import com.staymart.dto.response.WishlistResponse;
import com.staymart.entity.Property;
import com.staymart.entity.Product;
import com.staymart.entity.User;
import com.staymart.entity.Wishlist;
import com.staymart.entity.enums.BehaviorAction;
import com.staymart.entity.enums.BehaviorItemType;
import com.staymart.entity.enums.WishlistItemType;
import com.staymart.exception.BadRequestException;
import com.staymart.repository.PropertyRepository;
import com.staymart.repository.ProductRepository;
import com.staymart.repository.WishlistRepository;
import com.staymart.util.SecurityUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.Optional;

@Service
public class WishlistService {

    private final WishlistRepository wishlistRepository;
    private final PropertyRepository propertyRepository;
    private final ProductRepository productRepository;
    private final BehaviorService behaviorService;

    public WishlistService(WishlistRepository wishlistRepository,
                           PropertyRepository propertyRepository,
                           ProductRepository productRepository,
                           BehaviorService behaviorService) {
        this.wishlistRepository = wishlistRepository;
        this.propertyRepository = propertyRepository;
        this.productRepository = productRepository;
        this.behaviorService = behaviorService;
    }

    @Transactional
    public WishlistResponse add(WishlistRequest request) {
        User user = SecurityUtils.currentUser();

        Optional<Wishlist> existing = wishlistRepository
                .findByUserIdAndItemTypeAndItemId(user.getId(), request.itemType(), request.itemId());
        if (existing.isPresent()) {
            return toResponse(existing.get());
        }

        Wishlist wishlist = Wishlist.builder()
                .user(user)
                .itemType(request.itemType())
                .itemId(request.itemId())
                .build();
        Wishlist saved = wishlistRepository.save(wishlist);

        behaviorService.record(user.getId(), convert(request.itemType()), request.itemId(),
                BehaviorAction.WISHLIST, null, null);
        return toResponse(saved);
    }

    @Transactional
    public void remove(WishlistItemType itemType, Long itemId) {
        Long userId = SecurityUtils.currentUserId();
        wishlistRepository.deleteByUserIdAndItemTypeAndItemId(userId, itemType, itemId);
    }

    @Transactional(readOnly = true)
    public PageResponse<WishlistResponse> list(Pageable pageable) {
        Page<Wishlist> page = wishlistRepository.findByUserId(SecurityUtils.currentUserId(), pageable);
        return PageResponse.of(page, this::toResponse);
    }

    @Transactional(readOnly = true)
    public boolean isInWishlist(WishlistItemType itemType, Long itemId) {
        return wishlistRepository.existsByUserIdAndItemTypeAndItemId(
                SecurityUtils.currentUserId(), itemType, itemId);
    }

    @Transactional(readOnly = true)
    public WishlistResponse toResponse(Wishlist wishlist) {
        String title = null;
        String image = null;
        BigDecimal price = null;

        if (wishlist.getItemType() == WishlistItemType.PROPERTY) {
            Property property = propertyRepository.findById(wishlist.getItemId()).orElse(null);
            if (property != null) {
                title = property.getTitle();
                image = property.getImages() == null || property.getImages().isEmpty()
                        ? null : property.getImages().get(0);
                price = property.getPricePerMonth();
            }
        } else {
            Product product = productRepository.findById(wishlist.getItemId()).orElse(null);
            if (product != null) {
                title = product.getTitle();
                image = product.getImages() == null || product.getImages().isEmpty()
                        ? null : product.getImages().get(0);
                price = product.getPrice();
            }
        }

        if (title == null) {
            throw new BadRequestException("Wishlisted item no longer exists");
        }

        return new WishlistResponse(wishlist.getId(), wishlist.getItemType(), wishlist.getItemId(),
                title, image, price, wishlist.getCreatedAt());
    }

    private BehaviorItemType convert(WishlistItemType type) {
        return type == WishlistItemType.PROPERTY ? BehaviorItemType.PROPERTY : BehaviorItemType.PRODUCT;
    }
}