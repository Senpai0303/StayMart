package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.WishlistRequest;
import com.staymart.dto.response.WishlistResponse;
import com.staymart.entity.enums.WishlistItemType;
import com.staymart.service.WishlistService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/wishlist")
@Tag(name = "Wishlist", description = "Saved properties and products")
@SecurityRequirement(name = "bearerAuth")
public class WishlistController {

    private final WishlistService wishlistService;

    public WishlistController(WishlistService wishlistService) {
        this.wishlistService = wishlistService;
    }

    @GetMapping
    @Operation(summary = "List my saved items")
    public ApiResponse<PageResponse<WishlistResponse>> list(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(wishlistService.list(pageable(page, size)));
    }

    @PostMapping
    @Operation(summary = "Save an item to wishlist")
    public ApiResponse<WishlistResponse> add(@Valid @RequestBody WishlistRequest request) {
        return ApiResponse.ok("Item saved", wishlistService.add(request));
    }

    @DeleteMapping
    @Operation(summary = "Remove an item from wishlist")
    public ApiResponse<Void> remove(@RequestParam WishlistItemType itemType,
                                    @RequestParam Long itemId) {
        wishlistService.remove(itemType, itemId);
        return ApiResponse.ok("Item removed from wishlist", null);
    }

    @GetMapping("/check")
    @Operation(summary = "Check if an item is in my wishlist")
    public ApiResponse<Boolean> check(@RequestParam WishlistItemType itemType,
                                      @RequestParam Long itemId) {
        return ApiResponse.ok(wishlistService.isInWishlist(itemType, itemId));
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 100), Sort.by(Sort.Direction.DESC, "createdAt"));
    }
}