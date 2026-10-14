package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.dto.request.CategoryRequest;
import com.staymart.dto.response.CategoryResponse;
import com.staymart.entity.enums.CategoryType;
import com.staymart.service.CategoryService;
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
@RequestMapping("/api/categories")
@Tag(name = "Categories", description = "Category metadata")
public class CategoryController {

    private final CategoryService categoryService;

    public CategoryController(CategoryService categoryService) {
        this.categoryService = categoryService;
    }

    @GetMapping
    public ApiResponse<List<CategoryResponse>> findAll(@RequestParam(required = false) CategoryType type) {
        return ApiResponse.ok(categoryService.findAll(type));
    }

    @GetMapping("/{id}")
    public ApiResponse<CategoryResponse> getById(@PathVariable Long id) {
        return ApiResponse.ok(categoryService.getById(id));
    }

    @PostMapping
    @Operation(summary = "Create a category", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<CategoryResponse> create(@Valid @RequestBody CategoryRequest request) {
        return ApiResponse.ok("Category created", categoryService.create(request));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update a category", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<CategoryResponse> update(@PathVariable Long id,
                                                @Valid @RequestBody CategoryRequest request) {
        return ApiResponse.ok("Category updated", categoryService.update(id, request));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a category", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<Void> delete(@PathVariable Long id) {
        categoryService.delete(id);
        return ApiResponse.ok("Category deleted", null);
    }
}