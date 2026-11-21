package com.staymart.security;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockHttpServletRequest;

import static org.junit.jupiter.api.Assertions.*;

public class JwtAuthenticationFilterTest {

    private JwtAuthenticationFilter filter;

    @BeforeEach
    void setUp() {
        // JwtService and CustomUserDetailsService are only needed during doFilterInternal token parsing
        filter = new JwtAuthenticationFilter(null, null);
    }

    @Test
    @DisplayName("shouldNotFilter returns true for OPTIONS preflight requests")
    void testOptionsShouldNotFilter() {
        MockHttpServletRequest request = new MockHttpServletRequest("OPTIONS", "/api/properties");
        assertTrue(filter.shouldNotFilter(request));
    }

    @Test
    @DisplayName("shouldNotFilter returns true for static uploads and swagger docs")
    void testStaticAndDocsBypassed() {
        MockHttpServletRequest req1 = new MockHttpServletRequest("GET", "/uploads/test.jpg");
        assertTrue(filter.shouldNotFilter(req1));

        MockHttpServletRequest req2 = new MockHttpServletRequest("GET", "/swagger-ui/index.html");
        assertTrue(filter.shouldNotFilter(req2));

        MockHttpServletRequest req3 = new MockHttpServletRequest("GET", "/v3/api-docs");
        assertTrue(filter.shouldNotFilter(req3));
    }

    @Test
    @DisplayName("shouldNotFilter returns false for API endpoints so Authorization token is processed")
    void testApiEndpointsAreFiltered() {
        MockHttpServletRequest req1 = new MockHttpServletRequest("GET", "/api/properties");
        assertFalse(filter.shouldNotFilter(req1));

        MockHttpServletRequest req2 = new MockHttpServletRequest("GET", "/api/recommendations/properties");
        assertFalse(filter.shouldNotFilter(req2));

        MockHttpServletRequest req3 = new MockHttpServletRequest("POST", "/api/bookings");
        assertFalse(filter.shouldNotFilter(req3));
    }
}
