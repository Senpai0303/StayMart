package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.BookingRequest;
import com.staymart.dto.response.BookingResponse;
import com.staymart.entity.enums.BookingStatus;
import com.staymart.service.BookingService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/bookings")
@Tag(name = "Bookings", description = "Property/room booking requests")
@SecurityRequirement(name = "bearerAuth")
public class BookingController {

    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;
    }

    @PostMapping
    @Operation(summary = "Create a booking request")
    public ApiResponse<BookingResponse> create(@Valid @RequestBody BookingRequest request) {
        return ApiResponse.ok("Booking request sent", bookingService.create(request));
    }

    @GetMapping("/mine")
    @Operation(summary = "List bookings placed by me")
    public ApiResponse<PageResponse<BookingResponse>> getMyBookings(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(bookingService.getMyBookings(pageable(page, size)));
    }

    @GetMapping("/incoming")
    @Operation(summary = "List booking requests received on my properties")
    public ApiResponse<PageResponse<BookingResponse>> getIncoming(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ApiResponse.ok(bookingService.getIncomingBookings(pageable(page, size)));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get a booking by id")
    public ApiResponse<BookingResponse> getById(@PathVariable Long id) {
        return ApiResponse.ok(bookingService.getById(id));
    }

    @PatchMapping("/{id}/status")
    @Operation(summary = "Update booking status (owner/admin)")
    public ApiResponse<BookingResponse> updateStatus(@PathVariable Long id,
                                                     @RequestParam BookingStatus status) {
        return ApiResponse.ok("Booking status updated", bookingService.updateStatus(id, status));
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 100), Sort.by(Sort.Direction.DESC, "createdAt"));
    }
}