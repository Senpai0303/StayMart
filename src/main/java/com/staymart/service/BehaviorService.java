package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.BehaviorRequest;
import com.staymart.dto.response.BehaviorHistoryResponse;
import com.staymart.dto.response.RecommendationResponse;
import com.staymart.entity.User;
import com.staymart.entity.enums.BehaviorAction;
import com.staymart.entity.enums.BehaviorItemType;
import com.staymart.entity.UserBehavior;
import com.staymart.repository.UserRepository;
import com.staymart.repository.UserBehaviorRepository;
import com.staymart.util.SecurityUtils;
import org.springframework.context.annotation.Lazy;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

@Service
public class BehaviorService {

    private final UserBehaviorRepository behaviorRepository;
    private final UserRepository userRepository;
    private final PropertyService propertyService;
    private final ProductService productService;

    public BehaviorService(UserBehaviorRepository behaviorRepository,
                           UserRepository userRepository,
                           @Lazy PropertyService propertyService,
                           @Lazy ProductService productService) {
        this.behaviorRepository = behaviorRepository;
        this.userRepository = userRepository;
        this.propertyService = propertyService;
        this.productService = productService;
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void record(Long userId, BehaviorItemType itemType, Long itemId,
                       BehaviorAction action, String searchQuery, String cityFilter) {
        if (userId == null || itemId == null) {
            return;
        }
        userRepository.findById(userId).ifPresent(user -> {
            Long effectiveItemId = action == BehaviorAction.SEARCH ? 0L : itemId;
            behaviorRepository.save(UserBehavior.builder()
                    .user(user)
                    .itemType(itemType)
                    .itemId(effectiveItemId)
                    .action(action)
                    .searchQuery(searchQuery)
                    .cityFilter(cityFilter)
                    .timestamp(LocalDateTime.now())
                    .build());
        });
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void recordSearch(BehaviorItemType itemType, String searchQuery, String cityFilter) {
        record(SecurityUtils.currentUserIdOrNull(), itemType, 0L,
                BehaviorAction.SEARCH, searchQuery, cityFilter);
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void recordExplicit(BehaviorRequest request) {
        record(SecurityUtils.currentUser().getId(), request.itemType(), request.itemId(),
                request.action(), request.searchQuery(), request.cityFilter());
    }

    @Transactional(readOnly = true)
    public PageResponse<BehaviorHistoryResponse> getHistory(Pageable pageable) {
        Page<UserBehavior> page = behaviorRepository.findByUserId(SecurityUtils.currentUserId(), pageable);
        return PageResponse.of(page, BehaviorHistoryResponse::from);
    }

    @Transactional(readOnly = true)
    public RecommendationResponse recommendations(int limit) {
        Long userId = SecurityUtils.currentUserIdOrNull();
        if (userId == null) {
            return new RecommendationResponse(List.of(), List.of());
        }

        return new RecommendationResponse(recommendedProperties(userId, limit),
                recommendedProducts(userId, limit));
    }

    private List<com.staymart.dto.response.PropertyResponse> recommendedProperties(Long userId, int limit) {
        Set<Long> ids = new LinkedHashSet<>();
        List<com.staymart.dto.response.PropertyResponse> result = new ArrayList<>();
        List<UserBehavior> behaviors = behaviorRepository.findTop30ByUserIdOrderByTimestampDesc(userId);
        behaviors.stream()
                .filter(b -> b.getItemType() == com.staymart.entity.enums.BehaviorItemType.PROPERTY)
                .map(UserBehavior::getItemId)
                .forEach(ids::add);

        result.addAll(propertyService.findRecommendedProperties(new ArrayList<>(ids), limit));
        if (result.size() < limit) {
            propertyService.latestApproved(limit).stream()
                    .filter(p -> !ids.contains(p.id()))
                    .forEach(result::add);
        }
        return result.size() > limit ? result.subList(0, limit) : result;
    }

    private List<com.staymart.dto.response.ProductResponse> recommendedProducts(Long userId, int limit) {
        Set<Long> ids = new LinkedHashSet<>();
        List<com.staymart.dto.response.ProductResponse> result = new ArrayList<>();
        List<UserBehavior> behaviors = behaviorRepository.findTop30ByUserIdOrderByTimestampDesc(userId);
        behaviors.stream()
                .filter(b -> b.getItemType() == com.staymart.entity.enums.BehaviorItemType.PRODUCT)
                .map(UserBehavior::getItemId)
                .forEach(ids::add);

        result.addAll(productService.findRecommendedProducts(new ArrayList<>(ids), limit));
        if (result.size() < limit) {
            productService.latestApproved(limit).stream()
                    .filter(p -> !ids.contains(p.id()))
                    .forEach(result::add);
        }
        return result.size() > limit ? result.subList(0, limit) : result;
    }
}