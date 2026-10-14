package com.staymart.repository.spec;

import com.staymart.dto.request.ProductSearchCriteria;
import com.staymart.entity.Product;
import com.staymart.entity.enums.ModerationStatus;
import jakarta.persistence.criteria.Join;
import jakarta.persistence.criteria.JoinType;
import jakarta.persistence.criteria.Predicate;
import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;

public final class ProductSpecifications {

    private ProductSpecifications() {
    }

    public static Specification<Product> filter(ProductSearchCriteria criteria) {
        return (root, query, cb) -> {
            List<Predicate> predicates = new ArrayList<>();

            predicates.add(cb.equal(root.get("status"), ModerationStatus.APPROVED));

            if (Boolean.TRUE.equals(criteria.available())) {
                predicates.add(cb.isTrue(root.get("isAvailable")));
            }

            if (criteria.categoryId() != null) {
                predicates.add(cb.equal(root.get("category").get("id"), criteria.categoryId()));
            }

            if (criteria.listingType() != null) {
                predicates.add(cb.or(
                        cb.equal(root.get("listingType"), criteria.listingType()),
                        cb.equal(root.get("listingType"), com.staymart.entity.enums.ListingType.BOTH)
                ));
            }

            if (criteria.condition() != null) {
                predicates.add(cb.equal(root.get("condition"), criteria.condition()));
            }

            if (criteria.minPrice() != null) {
                predicates.add(cb.ge(root.get("price"), criteria.minPrice()));
            }

            if (criteria.maxPrice() != null) {
                predicates.add(cb.le(root.get("price"), criteria.maxPrice()));
            }

            if (criteria.area() != null && !criteria.area().isBlank()) {
                predicates.add(cb.like(cb.lower(root.get("area")), "%" + criteria.area().toLowerCase() + "%"));
            }

            if (criteria.city() != null && !criteria.city().isBlank()) {
                Join<Object, Object> location = root.join("location", JoinType.LEFT);
                predicates.add(cb.like(cb.lower(location.get("city")), "%" + criteria.city().toLowerCase() + "%"));
            }

            if (criteria.keyword() != null && !criteria.keyword().isBlank()) {
                String like = "%" + criteria.keyword().toLowerCase() + "%";
                predicates.add(cb.or(
                        cb.like(cb.lower(root.get("title")), like),
                        cb.like(cb.lower(root.get("description")), like),
                        cb.like(cb.lower(root.get("brand")), like)
                ));
            }

            return cb.and(predicates.toArray(new Predicate[0]));
        };
    }
}