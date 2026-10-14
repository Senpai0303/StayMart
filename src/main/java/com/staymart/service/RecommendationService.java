package com.staymart.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.staymart.dto.response.ProductResponse;
import com.staymart.dto.response.PropertyResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.ArrayList;
import java.util.List;

@Service
public class RecommendationService {

    private static final Logger log = LoggerFactory.getLogger(RecommendationService.class);
    private static final String DEFAULT_CITY = "Dehradun";

    private final RestClient client;
    private final ObjectMapper objectMapper;
    private final PropertyService propertyService;
    private final ProductService productService;

    public RecommendationService(RestClient.Builder builder,
                                 ObjectMapper objectMapper,
                                 PropertyService propertyService,
                                 ProductService productService,
                                 @Value("${app.ml.base-url:http://localhost:5000}") String mlBaseUrl) {
        this.client = builder.baseUrl(mlBaseUrl).build();
        this.objectMapper = objectMapper;
        this.propertyService = propertyService;
        this.productService = productService;
    }

    public List<PropertyResponse> recommendedProperties(Long userId, String city, int limit) {
        List<Long> ids = fetchItemIds("/recommend/properties?userId={userId}&city={city}&limit={limit}",
                userId == null ? 0L : userId, resolveCity(city), limit);
        if (ids.isEmpty()) {
            return propertyService.latestApproved(limit);
        }
        List<PropertyResponse> properties = propertyService.findRecommendedProperties(ids, limit);
        if (properties.isEmpty()) {
            return propertyService.latestApproved(limit);
        }
        return properties;
    }

    public List<ProductResponse> recommendedProducts(Long userId, String city, int limit) {
        List<Long> ids = fetchItemIds("/recommend/products?userId={userId}&city={city}&limit={limit}",
                userId == null ? 0L : userId, resolveCity(city), limit);
        if (ids.isEmpty()) {
            return productService.latestApproved(limit);
        }
        List<ProductResponse> products = productService.findRecommendedProducts(ids, limit);
        if (products.isEmpty()) {
            return productService.latestApproved(limit);
        }
        return products;
    }

    public List<PropertyResponse> similarProperties(Long propertyId, int limit) {
        List<Long> ids = fetchItemIds("/similar/property?propertyId={propertyId}&limit={limit}",
                propertyId, limit);
        List<PropertyResponse> properties = ids.isEmpty()
                ? List.of()
                : propertyService.findRecommendedProperties(ids, limit);
        if (properties.isEmpty()) {
            return propertyService.latestApproved(limit);
        }
        return properties;
    }

    public List<PropertyResponse> trendingProperties(String city, int limit) {
        List<Long> ids = fetchItemIds("/trending?type=PROPERTY&city={city}&limit={limit}",
                resolveCity(city), limit);
        List<PropertyResponse> properties = ids.isEmpty()
                ? List.of()
                : propertyService.findRecommendedProperties(ids, limit);
        if (properties.isEmpty()) {
            return propertyService.latestApproved(limit);
        }
        return properties;
    }

    public List<ProductResponse> trendingProducts(String city, int limit) {
        List<Long> ids = fetchItemIds("/trending?type=PRODUCT&city={city}&limit={limit}",
                resolveCity(city), limit);
        List<ProductResponse> products = ids.isEmpty()
                ? List.of()
                : productService.findRecommendedProducts(ids, limit);
        if (products.isEmpty()) {
            return productService.latestApproved(limit);
        }
        return products;
    }

    private List<Long> fetchItemIds(String uriTemplate, Object... variables) {
        try {
            String body = client.get().uri(uriTemplate, variables)
                    .retrieve()
                    .body(String.class);
            if (body == null || body.isBlank()) {
                return List.of();
            }
            JsonNode root = objectMapper.readTree(body);
            JsonNode items = root.path("items");
            if (!items.isArray()) {
                return List.of();
            }
            List<Long> ids = new ArrayList<>();
            for (JsonNode item : items) {
                JsonNode idNode = firstNumber(item, "id", "property_id", "product_id", "item_id");
                if (idNode != null) {
                    ids.add(idNode.asLong());
                }
            }
            return ids;
        } catch (Exception ex) {
            log.warn("ML service recommendation call failed ({}): {}", uriTemplate, ex.getMessage());
            return List.of();
        }
    }

    private JsonNode firstNumber(JsonNode node, String... fields) {
        for (String field : fields) {
            JsonNode value = node.get(field);
            if (value != null && value.isNumber()) {
                return value;
            }
        }
        return null;
    }

    private String resolveCity(String city) {
        return city == null || city.isBlank() ? DEFAULT_CITY : city;
    }
}
