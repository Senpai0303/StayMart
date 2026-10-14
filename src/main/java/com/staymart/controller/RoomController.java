package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.dto.request.RoomRequest;
import com.staymart.dto.response.RoomResponse;
import com.staymart.service.RoomService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/properties/{propertyId}/rooms")
@Tag(name = "Rooms", description = "Rooms within a property")
public class RoomController {

    private final RoomService roomService;

    public RoomController(RoomService roomService) {
        this.roomService = roomService;
    }

    @GetMapping
    @Operation(summary = "List rooms of a property")
    public ApiResponse<List<RoomResponse>> list(@PathVariable Long propertyId) {
        return ApiResponse.ok(roomService.listByProperty(propertyId));
    }

    @PostMapping
    @Operation(summary = "Add a room to a property", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<RoomResponse> add(@PathVariable Long propertyId,
                                         @Valid @RequestBody RoomRequest request) {
        return ApiResponse.ok("Room added", roomService.addRoom(propertyId, request));
    }

    @PutMapping("/{roomId}")
    @Operation(summary = "Update a room", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<RoomResponse> update(@PathVariable Long propertyId,
                                            @PathVariable Long roomId,
                                            @Valid @RequestBody RoomRequest request) {
        return ApiResponse.ok("Room updated", roomService.updateRoom(roomId, request));
    }

    @DeleteMapping("/{roomId}")
    @Operation(summary = "Delete a room", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<Void> delete(@PathVariable Long propertyId, @PathVariable Long roomId) {
        roomService.deleteRoom(roomId);
        return ApiResponse.ok("Room deleted", null);
    }
}