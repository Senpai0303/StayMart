package com.staymart.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.staymart.dto.response.ProductResponse;
import com.staymart.dto.response.PropertyResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.web.client.RestClient;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class RecommendationServiceTest {

    static class StubMlServiceClient extends MlServiceClient {
        List<Long> propIds = new ArrayList<>();
        List<Long> prodIds = new ArrayList<>();
        List<Long> simPropIds = new ArrayList<>();
        List<Long> simProdIds = new ArrayList<>();
        List<Long> trendPropIds = new ArrayList<>();
        List<Long> trendProdIds = new ArrayList<>();

        public StubMlServiceClient() {
            super(null, null, "http://localhost:5000");
        }

        @Override
        public List<Long> fetchRecommendedPropertyIds(Long userId, String city, int limit) {
            return propIds;
        }

        @Override
        public List<Long> fetchRecommendedProductIds(Long userId, String city, int limit) {
            return prodIds;
        }

        @Override
        public List<Long> fetchSimilarPropertyIds(Long propertyId, int limit) {
            return simPropIds;
        }

        @Override
        public List<Long> fetchSimilarProductIds(Long productId, int limit) {
            return simProdIds;
        }

        @Override
        public List<Long> fetchTrendingPropertyIds(String city, int limit) {
            return trendPropIds;
        }

        @Override
        public List<Long> fetchTrendingProductIds(String city, int limit) {
            return trendProdIds;
        }
    }

    static class StubPropertyService extends PropertyService {
        List<PropertyResponse> recommended = new ArrayList<>();
        List<PropertyResponse> latest = new ArrayList<>();
        int latestCalledCount = 0;

        public StubPropertyService() {
            super(null, null, null, null);
        }

        @Override
        public List<PropertyResponse> findRecommendedProperties(List<Long> ids, int limit) {
            return recommended;
        }

        @Override
        public List<PropertyResponse> latestApproved(int limit) {
            latestCalledCount++;
            return latest;
        }
    }

    static class StubProductService extends ProductService {
        List<ProductResponse> recommended = new ArrayList<>();
        List<ProductResponse> latest = new ArrayList<>();
        int latestCalledCount = 0;

        public StubProductService() {
            super(null, null, null, null);
        }

        @Override
        public List<ProductResponse> findRecommendedProducts(List<Long> ids, int limit) {
            return recommended;
        }

        @Override
        public List<ProductResponse> latestApproved(int limit) {
            latestCalledCount++;
            return latest;
        }
    }

    private StubMlServiceClient mlClient;
    private StubPropertyService propertyService;
    private StubProductService productService;
    private RecommendationService recommendationService;

    @BeforeEach
    void setUp() {
        mlClient = new StubMlServiceClient();
        propertyService = new StubPropertyService();
        productService = new StubProductService();
        recommendationService = new RecommendationService(mlClient, propertyService, productService);
    }

    @Test
    @DisplayName("recommendedProperties falls back to latestApproved when ML returns empty list")
    void testRecommendedPropertiesFallbackWhenMlEmpty() {
        mlClient.propIds = List.of();
        PropertyResponse fallback = new PropertyResponse(101L, "PG Fallback", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        propertyService.latest = List.of(fallback);

        List<PropertyResponse> result = recommendationService.recommendedProperties(1L, "Dehradun", 5);

        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(101L, result.get(0).id());
        assertEquals(1, propertyService.latestCalledCount);
    }

    @Test
    @DisplayName("recommendedProperties returns ML recommended properties when available")
    void testRecommendedPropertiesSuccess() {
        mlClient.propIds = List.of(10L, 20L);
        PropertyResponse p1 = new PropertyResponse(10L, "P1", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        PropertyResponse p2 = new PropertyResponse(20L, "P2", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        propertyService.recommended = List.of(p1, p2);

        List<PropertyResponse> result = recommendationService.recommendedProperties(1L, "Dehradun", 5);

        assertNotNull(result);
        assertEquals(2, result.size());
        assertEquals(10L, result.get(0).id());
        assertEquals(0, propertyService.latestCalledCount);
    }

    @Test
    @DisplayName("similarProperties falls back to latestApproved when ML returns no similar items")
    void testSimilarPropertiesFallback() {
        mlClient.simPropIds = List.of();
        PropertyResponse fallback = new PropertyResponse(99L, "Similar Fallback", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        propertyService.latest = List.of(fallback);

        List<PropertyResponse> result = recommendationService.similarProperties(42L, 4);

        assertEquals(1, result.size());
        assertEquals(99L, result.get(0).id());
        assertEquals(1, propertyService.latestCalledCount);
    }

    @Test
    @DisplayName("similarProducts returns ML recommendations or falls back gracefully")
    void testSimilarProducts() {
        mlClient.simProdIds = List.of(6L);
        ProductResponse pr = new ProductResponse(6L, "Product 6", null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        productService.recommended = List.of(pr);

        List<ProductResponse> result = recommendationService.similarProducts(5L, 3);
        assertEquals(1, result.size());
        assertEquals(6L, result.get(0).id());

        // Test fallback
        mlClient.simProdIds = List.of();
        ProductResponse fallbackProd = new ProductResponse(1L, "Fallback Product", null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        productService.latest = List.of(fallbackProd);

        List<ProductResponse> fallbackResult = recommendationService.similarProducts(999L, 3);
        assertEquals(1, fallbackResult.size());
        assertEquals(1L, fallbackResult.get(0).id());
        assertEquals(1, productService.latestCalledCount);
    }

    @Test
    @DisplayName("trendingProperties falls back when ML offline or empty")
    void testTrendingPropertiesFallback() {
        mlClient.trendPropIds = List.of();
        PropertyResponse fallback = new PropertyResponse(77L, "Trending Fallback", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        propertyService.latest = List.of(fallback);

        List<PropertyResponse> result = recommendationService.trendingProperties("Dehradun", 8);
        assertEquals(1, result.size());
        assertEquals(77L, result.get(0).id());
        assertEquals(1, propertyService.latestCalledCount);
    }

    @Test
    @DisplayName("trendingProducts falls back when ML offline or empty")
    void testTrendingProductsFallback() {
        mlClient.trendProdIds = List.of();
        ProductResponse fallback = new ProductResponse(88L, "Trending Prod Fallback", null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        productService.latest = List.of(fallback);

        List<ProductResponse> result = recommendationService.trendingProducts("Dehradun", 8);
        assertEquals(1, result.size());
        assertEquals(88L, result.get(0).id());
        assertEquals(1, productService.latestCalledCount);
    }
}
