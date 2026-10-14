package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.ProductRequest;
import com.staymart.dto.request.ProductSearchCriteria;
import com.staymart.dto.response.ProductResponse;
import com.staymart.entity.Product;
import com.staymart.entity.User;
import com.staymart.entity.enums.ListingType;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.entity.enums.ProductCondition;
import com.staymart.exception.AccessForbiddenException;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.CategoryRepository;
import com.staymart.repository.LocationRepository;
import com.staymart.repository.ProductRepository;
import com.staymart.repository.spec.ProductSpecifications;
import com.staymart.util.SecurityUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class ProductService {

    private final ProductRepository productRepository;
    private final CategoryRepository categoryRepository;
    private final LocationRepository locationRepository;
    private final BehaviorService behaviorService;

    public ProductService(ProductRepository productRepository,
                          CategoryRepository categoryRepository,
                          LocationRepository locationRepository,
                          BehaviorService behaviorService) {
        this.productRepository = productRepository;
        this.categoryRepository = categoryRepository;
        this.locationRepository = locationRepository;
        this.behaviorService = behaviorService;
    }

    @Transactional
    public ProductResponse create(ProductRequest request) {
        User user = SecurityUtils.currentUser();

        Product product = Product.builder()
                .postedBy(user)
                .category(request.categoryId() == null ? null
                        : categoryRepository.findById(request.categoryId())
                                .orElseThrow(() -> new BadRequestException("Category not found with id: " + request.categoryId())))
                .title(request.title().trim())
                .description(request.description())
                .price(request.price())
                .listingType(request.listingType() == null ? ListingType.SELL : request.listingType())
                .condition(request.condition() == null ? ProductCondition.GOOD : request.condition())
                .brand(request.brand())
                .location(request.locationId() == null ? null
                        : locationRepository.findById(request.locationId())
                                .orElseThrow(() -> new BadRequestException("Location not found with id: " + request.locationId())))
                .area(request.area())
                .images(request.images() == null ? List.of() : request.images())
                .status(ModerationStatus.PENDING)
                .isAvailable(true)
                .viewsCount(0)
                .build();

        return ProductResponse.from(productRepository.save(product));
    }

    @Transactional(readOnly = true)
    public ProductResponse getApproved(Long id) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
        if (product.getStatus() != ModerationStatus.APPROVED && !isOwnerOrAdmin(product)) {
            throw new ResourceNotFoundException("Product not found with id: " + id);
        }
        behaviorService.record(SecurityUtils.currentUserIdOrNull(),
                com.staymart.entity.enums.BehaviorItemType.PRODUCT, id,
                com.staymart.entity.enums.BehaviorAction.VIEW, null, product.getArea());

        product.setViewsCount(product.getViewsCount() + 1);
        productRepository.save(product);

        return ProductResponse.from(product);
    }

    @Transactional(readOnly = true)
    public ProductResponse getOwned(Long id) {
        Product product = findProduct(id);
        if (!isOwnerOrAdmin(product)) {
            throw new AccessForbiddenException("You can only view your own product details");
        }
        return ProductResponse.from(product);
    }

    @Transactional
    public ProductResponse update(Long id, ProductRequest request) {
        Product product = findProduct(id);
        if (!isOwnerOrAdmin(product)) {
            throw new AccessForbiddenException("You can only edit your own product");
        }

        product.setTitle(request.title().trim());
        product.setDescription(request.description());
        if (request.price() != null) {
            product.setPrice(request.price());
        }
        if (request.listingType() != null) {
            product.setListingType(request.listingType());
        }
        if (request.condition() != null) {
            product.setCondition(request.condition());
        }
        if (request.brand() != null) {
            product.setBrand(request.brand());
        }
        if (request.categoryId() != null) {
            product.setCategory(categoryRepository.findById(request.categoryId())
                    .orElseThrow(() -> new BadRequestException("Category not found with id: " + request.categoryId())));
        }
        if (request.locationId() != null) {
            product.setLocation(locationRepository.findById(request.locationId())
                    .orElseThrow(() -> new BadRequestException("Location not found with id: " + request.locationId())));
        }
        if (request.area() != null) {
            product.setArea(request.area());
        }
        if (request.images() != null) {
            product.setImages(request.images());
        }

        return ProductResponse.from(productRepository.save(product));
    }

    @Transactional
    public void delete(Long id) {
        Product product = findProduct(id);
        if (!isOwnerOrAdmin(product)) {
            throw new AccessForbiddenException("You can only delete your own product");
        }
        productRepository.delete(product);
    }

    @Transactional(readOnly = true)
    public PageResponse<ProductResponse> search(ProductSearchCriteria criteria) {
        Page<Product> page = productRepository.findAll(ProductSpecifications.filter(criteria), criteria.pageable());
        behaviorService.recordSearch(com.staymart.entity.enums.BehaviorItemType.PRODUCT,
                criteria.keyword(), criteria.city());
        return PageResponse.of(page, ProductResponse::from);
    }

    @Transactional(readOnly = true)
    public PageResponse<ProductResponse> listApproved(Pageable pageable) {
        Page<Product> page = productRepository.findByStatus(ModerationStatus.APPROVED, pageable);
        return PageResponse.of(page, ProductResponse::from);
    }

    @Transactional(readOnly = true)
    public List<ProductResponse> findRecommendedProducts(List<Long> ids, int limit) {
        List<Product> products = productRepository.findAllById(ids);
        return products.stream()
                .filter(p -> p.getStatus() == ModerationStatus.APPROVED)
                .map(ProductResponse::from)
                .limit(limit)
                .toList();
    }

    @Transactional(readOnly = true)
    public List<ProductResponse> latestApproved(int limit) {
        ProductSearchCriteria criteria = new ProductSearchCriteria(null, null, null, null,
                null, null, null, null, null,
                PageRequest.of(0, limit, Sort.by(Sort.Direction.DESC, "createdAt")));
        return productRepository.findAll(ProductSpecifications.filter(criteria), criteria.pageable())
                .map(ProductResponse::from)
                .getContent();
    }

    @Transactional(readOnly = true)
    public Product findProduct(Long id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
    }

    @Transactional(readOnly = true)
    public boolean isOwnerOrAdmin(Product product) {
        try {
            User current = SecurityUtils.currentUser();
            return current.getRole() == com.staymart.entity.enums.Role.ADMIN
                    || current.getId().equals(product.getPostedBy().getId());
        } catch (Exception ex) {
            return false;
        }
    }
}