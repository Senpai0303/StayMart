package com.staymart.repository;

import com.staymart.entity.Property;
import com.staymart.entity.enums.ModerationStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;

public interface PropertyRepository extends JpaRepository<Property, Long>, JpaSpecificationExecutor<Property> {

    Page<Property> findByStatus(ModerationStatus status, Pageable pageable);

    Page<Property> findByPostedById(Long userId, Pageable pageable);

    long countByStatus(ModerationStatus status);

    long countByPostedById(Long userId);

    @Query("SELECT p.type, COUNT(p) FROM Property p GROUP BY p.type ORDER BY COUNT(p) DESC")
    List<Object[]> countGroupByType();

    @Query("SELECT YEAR(p.createdAt), MONTH(p.createdAt), COUNT(p) FROM Property p "
            + "WHERE p.createdAt >= :since GROUP BY YEAR(p.createdAt), MONTH(p.createdAt) "
            + "ORDER BY YEAR(p.createdAt), MONTH(p.createdAt)")
    List<Object[]> countCreatedByMonthSince(@Param("since") LocalDateTime since);
}