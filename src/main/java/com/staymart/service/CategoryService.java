package com.staymart.service;

import com.staymart.dto.request.CategoryRequest;
import com.staymart.dto.response.CategoryResponse;
import com.staymart.entity.Category;
import com.staymart.entity.enums.CategoryType;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.DuplicateResourceException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.CategoryRepository;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class CategoryService {

    private final CategoryRepository categoryRepository;

    public CategoryService(CategoryRepository categoryRepository) {
        this.categoryRepository = categoryRepository;
    }

    @Transactional(readOnly = true)
    public List<CategoryResponse> findAll(CategoryType type) {
        List<Category> categories = type == null
                ? categoryRepository.findAll()
                : categoryRepository.findByType(type);
        return categories.stream().map(CategoryResponse::from).toList();
    }

    @Transactional(readOnly = true)
    public CategoryResponse getById(Long id) {
        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Category not found with id: " + id));
        return CategoryResponse.from(category);
    }

    @Transactional
    public CategoryResponse create(CategoryRequest request) {
        String name = request.name().trim();
        categoryRepository.findByNameAndType(name, request.type()).ifPresent(existing -> {
            throw new DuplicateResourceException("A " + request.type().name().toLowerCase()
                    + " category named '" + name + "' already exists");
        });
        Category category = Category.builder()
                .name(name)
                .type(request.type())
                .icon(request.icon())
                .parentId(request.parentId())
                .build();
        return CategoryResponse.from(categoryRepository.save(category));
    }

    @Transactional
    public CategoryResponse update(Long id, CategoryRequest request) {
        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Category not found with id: " + id));
        String name = request.name().trim();
        categoryRepository.findByNameAndType(name, request.type())
                .filter(existing -> !existing.getId().equals(id))
                .ifPresent(existing -> {
                    throw new DuplicateResourceException("A " + request.type().name().toLowerCase()
                            + " category named '" + name + "' already exists");
                });
        category.setName(name);
        category.setType(request.type());
        category.setIcon(request.icon());
        category.setParentId(request.parentId());
        return CategoryResponse.from(categoryRepository.save(category));
    }

    @Transactional
    public void delete(Long id) {
        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Category not found with id: " + id));
        try {
            categoryRepository.delete(category);
        } catch (DataIntegrityViolationException ex) {
            throw new BadRequestException("This category is in use by existing listings and cannot be deleted");
        }
    }
}