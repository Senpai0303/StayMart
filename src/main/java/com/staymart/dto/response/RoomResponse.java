package com.staymart.dto.response;

import com.staymart.entity.Room;
import com.staymart.entity.enums.RoomType;

import java.math.BigDecimal;
import java.util.List;

public record RoomResponse(
        Long id,
        Long propertyId,
        String roomNumber,
        RoomType type,
        BigDecimal price,
        Integer capacity,
        Integer floorNumber,
        Boolean isAvailable,
        List<String> images
) {
    public static RoomResponse from(Room room) {
        if (room == null) {
            return null;
        }
        return new RoomResponse(
                room.getId(),
                room.getProperty() == null ? null : room.getProperty().getId(),
                room.getRoomNumber(),
                room.getType(),
                room.getPrice(),
                room.getCapacity(),
                room.getFloorNumber(),
                room.getIsAvailable(),
                room.getImages()
        );
    }
}