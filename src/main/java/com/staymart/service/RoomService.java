package com.staymart.service;

import com.staymart.dto.request.RoomRequest;
import com.staymart.dto.response.RoomResponse;
import com.staymart.entity.Property;
import com.staymart.entity.Room;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.exception.AccessForbiddenException;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.RoomRepository;
import com.staymart.util.SecurityUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class RoomService {

    private final RoomRepository roomRepository;
    private final PropertyService propertyService;

    public RoomService(RoomRepository roomRepository, PropertyService propertyService) {
        this.roomRepository = roomRepository;
        this.propertyService = propertyService;
    }

    @Transactional(readOnly = true)
    public List<RoomResponse> listByProperty(Long propertyId) {
        Property property = propertyService.findProperty(propertyId);
        if (property.getStatus() != ModerationStatus.APPROVED && !propertyService.isOwnerOrAdmin(property)) {
            throw new ResourceNotFoundException("Property not found with id: " + propertyId);
        }
        return roomRepository.findByPropertyId(propertyId).stream().map(RoomResponse::from).toList();
    }

    @Transactional
    public RoomResponse addRoom(Long propertyId, RoomRequest request) {
        Property property = propertyService.findProperty(propertyId);
        if (!propertyService.isOwnerOrAdmin(property)) {
            throw new AccessForbiddenException("Only the property owner or admin can add rooms");
        }

        Room room = Room.builder()
                .property(property)
                .roomNumber(request.roomNumber())
                .type(request.type())
                .price(request.price())
                .capacity(request.capacity() == null ? 1 : request.capacity())
                .floorNumber(request.floorNumber() == null ? 0 : request.floorNumber())
                .isAvailable(request.isAvailable() == null ? Boolean.TRUE : request.isAvailable())
                .images(request.images() == null ? List.of() : request.images())
                .build();

        return RoomResponse.from(roomRepository.save(room));
    }

    @Transactional
    public RoomResponse updateRoom(Long roomId, RoomRequest request) {
        Room room = findRoom(roomId);
        if (!propertyService.isOwnerOrAdmin(room.getProperty())) {
            throw new AccessForbiddenException("Only the property owner or admin can edit rooms");
        }

        if (request.roomNumber() != null) {
            room.setRoomNumber(request.roomNumber());
        }
        if (request.type() != null) {
            room.setType(request.type());
        }
        if (request.price() != null) {
            room.setPrice(request.price());
        }
        if (request.capacity() != null) {
            room.setCapacity(request.capacity());
        }
        if (request.floorNumber() != null) {
            room.setFloorNumber(request.floorNumber());
        }
        if (request.isAvailable() != null) {
            room.setIsAvailable(request.isAvailable());
        }
        if (request.images() != null) {
            room.setImages(request.images());
        }

        return RoomResponse.from(roomRepository.save(room));
    }

    @Transactional
    public void deleteRoom(Long roomId) {
        Room room = findRoom(roomId);
        if (!propertyService.isOwnerOrAdmin(room.getProperty())) {
            throw new AccessForbiddenException("Only the property owner or admin can delete rooms");
        }
        roomRepository.delete(room);
    }

    @Transactional(readOnly = true)
    public Room findRoom(Long roomId) {
        return roomRepository.findById(roomId)
                .orElseThrow(() -> new ResourceNotFoundException("Room not found with id: " + roomId));
    }
}