package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.dto.request.LocationRequest;
import com.staymart.dto.response.LocationResponse;
import com.staymart.service.LocationService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/locations")
@Tag(name = "Locations", description = "Cities and areas in Uttarakhand")
public class LocationController {

    private final LocationService locationService;

    public LocationController(LocationService locationService) {
        this.locationService = locationService;
    }

    @GetMapping
    public ApiResponse<List<LocationResponse>> findAll() {
        return ApiResponse.ok(locationService.findAll());
    }

    @GetMapping("/cities")
    public ApiResponse<List<String>> listCities() {
        return ApiResponse.ok(locationService.listCities());
    }

    @GetMapping("/search")
    public ApiResponse<List<LocationResponse>> search(@RequestParam(required = false) String q,
                                                      @RequestParam(required = false) String city) {
        if (city != null && !city.isBlank()) {
            return ApiResponse.ok(locationService.findByCity(city));
        }
        return ApiResponse.ok(locationService.search(q == null ? "" : q));
    }

    @PostMapping
    @Operation(summary = "Create a location", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<LocationResponse> create(@Valid @RequestBody LocationRequest request) {
        return ApiResponse.ok("Location created", locationService.create(request));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update a location", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<LocationResponse> update(@PathVariable Long id,
                                                @Valid @RequestBody LocationRequest request) {
        return ApiResponse.ok("Location updated", locationService.update(id, request));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a location", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<Void> delete(@PathVariable Long id) {
        locationService.delete(id);
        return ApiResponse.ok("Location deleted", null);
    }
}