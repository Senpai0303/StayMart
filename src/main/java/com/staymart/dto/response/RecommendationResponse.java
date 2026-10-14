package com.staymart.dto.response;

import java.util.List;

public record RecommendationResponse(
        List<PropertyResponse> properties,
        List<ProductResponse> products
) {
}