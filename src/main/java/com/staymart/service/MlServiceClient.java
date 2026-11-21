package com.staymart.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.util.ArrayList;
import java.util.List;

@Component
public class MlServiceClient {

    private static final Logger log = LoggerFactory.getLogger(MlServiceClient.class);
    private static final int ML_CONNECT_TIMEOUT_MS = 2000;
    private static final int ML_READ_TIMEOUT_MS = 3000;

    private final RestClient client;
    private final ObjectMapper objectMapper;

    public MlServiceClient(RestClient.Builder builder,
                           ObjectMapper objectMapper,
                           @Value("${app.ml.base-url:http://localhost:5000}") String mlBaseUrl) {
        if (builder != null) {
            SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory();
            requestFactory.setConnectTimeout(ML_CONNECT_TIMEOUT_MS);
            requestFactory.setReadTimeout(ML_READ_TIMEOUT_MS);
            this.client = builder.baseUrl(mlBaseUrl).requestFactory(requestFactory).build();
        } else {
            this.client = null;
        }
        this.objectMapper = objectMapper;
    }

    public List<Long> fetchRecommendedPropertyIds(Long userId, String city, int limit) {
        return fetchIds("/recommend/properties/{userId}?city={city}&limit={limit}",
                userId == null ? 0L : userId, city, limit);
    }

    public List<Long> fetchRecommendedProductIds(Long userId, String city, int limit) {
        return fetchIds("/recommend/products/{userId}?city={city}&limit={limit}",
                userId == null ? 0L : userId, city, limit);
    }

    public List<Long> fetchSimilarPropertyIds(Long propertyId, int limit) {
        return fetchIds("/similar/property?propertyId={propertyId}&limit={limit}", propertyId, limit);
    }

    public List<Long> fetchSimilarProductIds(Long productId, int limit) {
        return fetchIds("/similar/product?productId={productId}&limit={limit}", productId, limit);
    }

    public List<Long> fetchTrendingPropertyIds(String city, int limit) {
        return fetchIds("/trending?type=PROPERTY&city={city}&limit={limit}", city, limit);
    }

    public List<Long> fetchTrendingProductIds(String city, int limit) {
        return fetchIds("/trending?type=PRODUCT&city={city}&limit={limit}", city, limit);
    }

    private List<Long> fetchIds(String uriTemplate, Object... variables) {
        try {
            String body = client.get().uri(uriTemplate, variables)
                    .retrieve()
                    .body(String.class);
            if (body == null || body.isBlank()) {
                log.error("ML service returned an empty response for {}", uriTemplate);
                return List.of();
            }
            return parseIds(objectMapper.readTree(body));
        } catch (RestClientException ex) {
            log.error("ML service connection failed for {}: {}", uriTemplate, ex.getMessage(), ex);
            return List.of();
        } catch (JsonProcessingException ex) {
            log.error("ML service returned invalid JSON for {}: {}", uriTemplate, ex.getMessage(), ex);
            return List.of();
        }
    }

    private List<Long> parseIds(JsonNode root) {
        if (root.isArray()) {
            return extractIds(root);
        }
        if (!root.isObject()) {
            log.error("Unexpected ML response shape: {}", root.getNodeType());
            return List.of();
        }

        for (String key : List.of("property_ids", "product_ids", "ids")) {
            JsonNode node = root.get(key);
            if (node != null && node.isArray()) {
                return extractIds(node);
            }
        }

        JsonNode items = root.path("items");
        if (items.isArray()) {
            return extractIds(items);
        }

        log.error("ML response did not contain an ID array: {}", root);
        return List.of();
    }

    private List<Long> extractIds(JsonNode array) {
        List<Long> ids = new ArrayList<>();
        for (JsonNode node : array) {
            if (node.isNumber()) {
                ids.add(node.asLong());
                continue;
            }
            if (node.isObject()) {
                for (String field : List.of("id", "property_id", "product_id", "item_id")) {
                    JsonNode value = node.get(field);
                    if (value != null && value.isNumber()) {
                        ids.add(value.asLong());
                        break;
                    }
                }
            }
        }
        return ids;
    }
}
