package com.staymart.service;

import com.staymart.dto.response.ProductResponse;
import com.staymart.dto.response.PropertyResponse;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RecommendationService {

    private static final String DEFAULT_CITY = "Dehradun";

    private final MlServiceClient mlServiceClient;
    private final PropertyService propertyService;
    private final ProductService productService;

    public RecommendationService(MlServiceClient mlServiceClient,
                                 PropertyService propertyService,
                                 ProductService productService) {
        this.mlServiceClient = mlServiceClient;
        this.propertyService = propertyService;
        this.productService = productService;
    }

    public List<PropertyResponse> recommendedProperties(Long userId, String city, int limit) {
        List<Long> ids = mlServiceClient.fetchRecommendedPropertyIds(userId, resolveCity(city), limit);
        List<PropertyResponse> properties = ids.isEmpty()
                ? List.of()
                : propertyService.findRecommendedProperties(ids, limit);
        if (properties.isEmpty()) {
            return propertyService.latestApproved(limit);
        }
        return properties;
    }

    public List<ProductResponse> recommendedProducts(Long userId, String city, int limit) {
        List<Long> ids = mlServiceClient.fetchRecommendedProductIds(userId, resolveCity(city), limit);
        List<ProductResponse> products = ids.isEmpty()
                ? List.of()
                : productService.findRecommendedProducts(ids, limit);
        if (products.isEmpty()) {
            return productService.latestApproved(limit);
        }
        return products;
    }

    public List<PropertyResponse> similarProperties(Long propertyId, int limit) {
        List<Long> ids = mlServiceClient.fetchSimilarPropertyIds(propertyId, limit);
        List<PropertyResponse> properties = ids.isEmpty()
                ? List.of()
                : propertyService.findRecommendedProperties(ids, limit);
        if (properties.isEmpty()) {
            return propertyService.latestApproved(limit);
        }
        return properties;
    }

    public List<ProductResponse> similarProducts(Long productId, int limit) {
        List<Long> ids = mlServiceClient.fetchSimilarProductIds(productId, limit);
        List<ProductResponse> products = ids.isEmpty()
                ? List.of()
                : productService.findRecommendedProducts(ids, limit);
        if (products.isEmpty()) {
            return productService.latestApproved(limit);
        }
        return products;
    }

    public List<PropertyResponse> trendingProperties(String city, int limit) {
        List<Long> ids = mlServiceClient.fetchTrendingPropertyIds(resolveCity(city), limit);
        List<PropertyResponse> properties = ids.isEmpty()
                ? List.of()
                : propertyService.findRecommendedProperties(ids, limit);
        if (properties.isEmpty()) {
            return propertyService.latestApproved(limit);
        }
        return properties;
    }

    public List<ProductResponse> trendingProducts(String city, int limit) {
        List<Long> ids = mlServiceClient.fetchTrendingProductIds(resolveCity(city), limit);
        List<ProductResponse> products = ids.isEmpty()
                ? List.of()
                : productService.findRecommendedProducts(ids, limit);
        if (products.isEmpty()) {
            return productService.latestApproved(limit);
        }
        return products;
    }

    private String resolveCity(String city) {
        return city == null || city.isBlank() ? DEFAULT_CITY : city;
    }
}
