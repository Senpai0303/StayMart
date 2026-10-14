package com.staymart.repository;

import com.staymart.entity.Review;
import com.staymart.entity.enums.ReviewItemType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ReviewRepository extends JpaRepository<Review, Long> {

    Page<Review> findByItemTypeAndItemId(ReviewItemType itemType, Long itemId, Pageable pageable);

    Page<Review> findByReviewerId(Long reviewerId, Pageable pageable);

    boolean existsByReviewerIdAndItemTypeAndItemId(Long reviewerId, ReviewItemType itemType, Long itemId);

    @Query("SELECT AVG(r.rating) FROM Review r WHERE r.itemType = :itemType AND r.itemId = :itemId")
    Double averageRating(@Param("itemType") ReviewItemType itemType, @Param("itemId") Long itemId);

    @Query("SELECT COUNT(r) FROM Review r WHERE r.itemType = :itemType AND r.itemId = :itemId")
    long countByItem(@Param("itemType") ReviewItemType itemType, @Param("itemId") Long itemId);

    List<Review> findByItemTypeAndItemId(ReviewItemType itemType, Long itemId);
}