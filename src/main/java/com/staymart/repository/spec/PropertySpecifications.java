package com.staymart.repository.spec;

import com.staymart.dto.request.PropertySearchCriteria;
import com.staymart.entity.Property;
import com.staymart.entity.enums.ModerationStatus;
import jakarta.persistence.criteria.Join;
import jakarta.persistence.criteria.JoinType;
import jakarta.persistence.criteria.Predicate;
import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;

public final class PropertySpecifications {

    private PropertySpecifications() {
    }

    public static Specification<Property> filter(PropertySearchCriteria criteria) {
        return (root, query, cb) -> {
            List<Predicate> predicates = new ArrayList<>();

            predicates.add(cb.equal(root.get("status"), ModerationStatus.APPROVED));

            if (Boolean.TRUE.equals(criteria.available())) {
                predicates.add(cb.isTrue(root.get("isAvailable")));
            }

            if (criteria.type() != null) {
                predicates.add(cb.equal(root.get("type"), criteria.type()));
            }

            if (criteria.genderPreference() != null) {
                predicates.add(cb.equal(root.get("genderPreference"), criteria.genderPreference()));
            }

            if (criteria.area() != null && !criteria.area().isBlank()) {
                predicates.add(cb.like(cb.lower(root.get("area")), "%" + criteria.area().toLowerCase() + "%"));
            }

            if (criteria.city() != null && !criteria.city().isBlank()) {
                Join<Object, Object> location = root.join("location", JoinType.LEFT);
                predicates.add(cb.like(cb.lower(location.get("city")), "%" + criteria.city().toLowerCase() + "%"));
            }

            if (criteria.minPrice() != null) {
                predicates.add(cb.ge(root.get("pricePerMonth"), criteria.minPrice()));
            }

            if (criteria.maxPrice() != null) {
                predicates.add(cb.le(root.get("pricePerMonth"), criteria.maxPrice()));
            }

            if (criteria.keyword() != null && !criteria.keyword().isBlank()) {
                String like = "%" + criteria.keyword().toLowerCase() + "%";
                predicates.add(cb.or(
                        cb.like(cb.lower(root.get("title")), like),
                        cb.like(cb.lower(root.get("description")), like),
                        cb.like(cb.lower(root.get("area")), like)
                ));
            }

            return cb.and(predicates.toArray(new Predicate[0]));
        };
    }
}