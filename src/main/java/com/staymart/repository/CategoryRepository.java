package com.staymart.repository;

import com.staymart.entity.Category;
import com.staymart.entity.enums.CategoryType;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface CategoryRepository extends JpaRepository<Category, Long> {

    List<Category> findByType(CategoryType type);

    Optional<Category> findByNameAndType(String name, CategoryType type);
}