package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.ProductRequest;
import com.staymart.dto.request.ProductSearchCriteria;
import com.staymart.dto.response.ProductResponse;
import com.staymart.entity.enums.ListingType;
import com.staymart.entity.enums.ProductCondition;
import com.staymart.service.ProductService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;

@RestController
@RequestMapping("/api/products")
@Tag(name = "Products", description = "Local marketplace listings (buy/sell/rent)")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping
    @Operation(summary = "Search approved products")
    public ApiResponse<PageResponse<ProductResponse>> search(
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) ListingType listingType,
            @RequestParam(required = false) ProductCondition condition,
            @RequestParam(required = false) BigDecimal minPrice,
            @RequestParam(required = false) BigDecimal maxPrice,
            @RequestParam(required = false) String area,
            @RequestParam(required = false) String city,
            @RequestParam(required = false) String q,
            @RequestParam(required = false, defaultValue = "true") Boolean available,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "12") int size) {
        ProductSearchCriteria criteria = new ProductSearchCriteria(
                categoryId, listingType, condition, minPrice, maxPrice, area, city, q, available,
                pageable(page, size));
        return ApiResponse.ok(productService.search(criteria));
    }

    @PostMapping
    @Operation(summary = "Post a new product listing", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<ProductResponse> create(@Valid @RequestBody ProductRequest request) {
        return ApiResponse.ok("Product submitted for review", productService.create(request));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get an approved product by id")
    public ApiResponse<ProductResponse> getById(@PathVariable Long id) {
        return ApiResponse.ok(productService.getApproved(id));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update own product", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<ProductResponse> update(@PathVariable Long id,
                                               @Valid @RequestBody ProductRequest request) {
        return ApiResponse.ok("Product updated", productService.update(id, request));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete own product", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<Void> delete(@PathVariable Long id) {
        productService.delete(id);
        return ApiResponse.ok("Product deleted", null);
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 50), Sort.by(Sort.Direction.DESC, "createdAt"));
    }
}