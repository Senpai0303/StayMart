package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.PropertyRequest;
import com.staymart.dto.request.PropertySearchCriteria;
import com.staymart.dto.response.PropertyResponse;
import com.staymart.entity.enums.GenderPreference;
import com.staymart.entity.enums.PropertyType;
import com.staymart.service.PropertyService;
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
@RequestMapping("/api/properties")
@Tag(name = "Properties", description = "Accommodation listings (PG, Rooms, Hostels, Hotels)")
public class PropertyController {

    private final PropertyService propertyService;

    public PropertyController(PropertyService propertyService) {
        this.propertyService = propertyService;
    }

    @GetMapping
    @Operation(summary = "Search approved properties")
    public ApiResponse<PageResponse<PropertyResponse>> search(
            @RequestParam(required = false) PropertyType type,
            @RequestParam(required = false) String city,
            @RequestParam(required = false) String area,
            @RequestParam(required = false) GenderPreference gender,
            @RequestParam(required = false) BigDecimal minPrice,
            @RequestParam(required = false) BigDecimal maxPrice,
            @RequestParam(required = false) String q,
            @RequestParam(required = false, defaultValue = "true") Boolean available,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "12") int size) {
        PropertySearchCriteria criteria = new PropertySearchCriteria(
                type, city, area, gender, minPrice, maxPrice, q, available, pageable(page, size));
        return ApiResponse.ok(propertyService.search(criteria));
    }

    @PostMapping
    @Operation(summary = "Post a new property listing", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<PropertyResponse> create(@Valid @RequestBody PropertyRequest request) {
        return ApiResponse.ok("Property submitted for review", propertyService.create(request));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get an approved property by id")
    public ApiResponse<PropertyResponse> getById(@PathVariable Long id) {
        return ApiResponse.ok(propertyService.getApproved(id));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update own property", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<PropertyResponse> update(@PathVariable Long id,
                                                @Valid @RequestBody PropertyRequest request) {
        return ApiResponse.ok("Property updated", propertyService.update(id, request));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete own property", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<Void> delete(@PathVariable Long id) {
        propertyService.delete(id);
        return ApiResponse.ok("Property deleted", null);
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 50), Sort.by(Sort.Direction.DESC, "createdAt"));
    }
}