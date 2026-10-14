package com.staymart.repository;

import com.staymart.entity.UserBehavior;
import com.staymart.entity.enums.BehaviorItemType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface UserBehaviorRepository extends JpaRepository<UserBehavior, Long> {

    List<UserBehavior> findTop30ByUserIdOrderByTimestampDesc(Long userId);

    Page<UserBehavior> findByUserId(Long userId, Pageable pageable);

    @Query("SELECT ub.itemId, COUNT(ub) FROM UserBehavior ub WHERE ub.itemType = :itemType AND ub.action = 'VIEW' GROUP BY ub.itemId ORDER BY COUNT(ub) DESC")
    List<Object[]> mostViewedItemIds(@Param("itemType") BehaviorItemType itemType, Pageable pageable);
}