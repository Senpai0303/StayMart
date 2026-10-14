package com.staymart.repository;

import com.staymart.entity.Wishlist;
import com.staymart.entity.enums.WishlistItemType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface WishlistRepository extends JpaRepository<Wishlist, Long> {

    Page<Wishlist> findByUserId(Long userId, Pageable pageable);

    Optional<Wishlist> findByUserIdAndItemTypeAndItemId(Long userId, WishlistItemType itemType, Long itemId);

    boolean existsByUserIdAndItemTypeAndItemId(Long userId, WishlistItemType itemType, Long itemId);

    void deleteByUserIdAndItemTypeAndItemId(Long userId, WishlistItemType itemType, Long itemId);
}