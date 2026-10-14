package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.PropertyRequest;
import com.staymart.dto.request.PropertySearchCriteria;
import com.staymart.dto.response.PropertyResponse;
import com.staymart.entity.Property;
import com.staymart.entity.Room;
import com.staymart.entity.User;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.exception.AccessForbiddenException;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.LocationRepository;
import com.staymart.repository.PropertyRepository;
import com.staymart.repository.RoomRepository;
import com.staymart.repository.spec.PropertySpecifications;
import com.staymart.util.SecurityUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class PropertyService {

    private final PropertyRepository propertyRepository;
    private final LocationRepository locationRepository;
    private final RoomRepository roomRepository;
    private final BehaviorService behaviorService;

    public PropertyService(PropertyRepository propertyRepository,
                           LocationRepository locationRepository,
                           RoomRepository roomRepository,
                           BehaviorService behaviorService) {
        this.propertyRepository = propertyRepository;
        this.locationRepository = locationRepository;
        this.roomRepository = roomRepository;
        this.behaviorService = behaviorService;
    }

    @Transactional
    public PropertyResponse create(PropertyRequest request) {
        User user = SecurityUtils.currentUser();

        Property property = Property.builder()
                .postedBy(user)
                .title(request.title().trim())
                .description(request.description())
                .type(request.type())
                .genderPreference(request.genderPreference() == null
                        ? com.staymart.entity.enums.GenderPreference.ANY
                        : request.genderPreference())
                .address(request.address())
                .area(request.area())
                .location(request.locationId() == null ? null
                        : locationRepository.findById(request.locationId())
                                .orElseThrow(() -> new BadRequestException("Location not found with id: " + request.locationId())))
                .pricePerMonth(request.pricePerMonth())
                .depositAmount(request.depositAmount() == null ? java.math.BigDecimal.ZERO : request.depositAmount())
                .amenities(request.amenities() == null ? List.of() : request.amenities())
                .totalRooms(request.totalRooms() == null ? 1 : request.totalRooms())
                .availableRooms(request.availableRooms() == null ? 1 : request.availableRooms())
                .images(request.images() == null ? List.of() : request.images())
                .status(ModerationStatus.PENDING)
                .isAvailable(true)
                .build();

        return PropertyResponse.from(propertyRepository.save(property));
    }

    @Transactional(readOnly = true)
    public PropertyResponse getApproved(Long id) {
        Property property = propertyRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Property not found with id: " + id));
        if (property.getStatus() != ModerationStatus.APPROVED && !isOwnerOrAdmin(property)) {
            throw new ResourceNotFoundException("Property not found with id: " + id);
        }
        behaviorService.record(SecurityUtils.currentUserIdOrNull(),
                com.staymart.entity.enums.BehaviorItemType.PROPERTY, id,
                com.staymart.entity.enums.BehaviorAction.VIEW, null, property.getArea());
        return PropertyResponse.from(property);
    }

    @Transactional(readOnly = true)
    public PropertyResponse getOwned(Long id) {
        Property property = findProperty(id);
        if (!isOwnerOrAdmin(property)) {
            throw new AccessForbiddenException("You can only view your own property details");
        }
        return PropertyResponse.from(property);
    }

    @Transactional
    public PropertyResponse update(Long id, PropertyRequest request) {
        Property property = findProperty(id);
        if (!isOwnerOrAdmin(property)) {
            throw new AccessForbiddenException("You can only edit your own property");
        }

        property.setTitle(request.title().trim());
        property.setDescription(request.description());
        property.setType(request.type());
        if (request.genderPreference() != null) {
            property.setGenderPreference(request.genderPreference());
        }
        property.setAddress(request.address());
        property.setArea(request.area());
        if (request.locationId() != null) {
            property.setLocation(locationRepository.findById(request.locationId())
                    .orElseThrow(() -> new BadRequestException("Location not found with id: " + request.locationId())));
        }
        if (request.pricePerMonth() != null) {
            property.setPricePerMonth(request.pricePerMonth());
        }
        if (request.depositAmount() != null) {
            property.setDepositAmount(request.depositAmount());
        }
        if (request.amenities() != null) {
            property.setAmenities(request.amenities());
        }
        if (request.totalRooms() != null) {
            property.setTotalRooms(request.totalRooms());
        }
        if (request.availableRooms() != null) {
            property.setAvailableRooms(request.availableRooms());
        }
        if (request.images() != null) {
            property.setImages(request.images());
        }

        return PropertyResponse.from(propertyRepository.save(property));
    }

    @Transactional
    public void delete(Long id) {
        Property property = findProperty(id);
        if (!isOwnerOrAdmin(property)) {
            throw new AccessForbiddenException("You can only delete your own property");
        }
        propertyRepository.delete(property);
    }

    @Transactional(readOnly = true)
    public PageResponse<PropertyResponse> search(PropertySearchCriteria criteria) {
        Page<Property> page = propertyRepository.findAll(PropertySpecifications.filter(criteria), criteria.pageable());
        behaviorService.recordSearch(com.staymart.entity.enums.BehaviorItemType.PROPERTY,
                criteria.keyword(), criteria.city());
        return PageResponse.of(page, PropertyResponse::from);
    }

    @Transactional(readOnly = true)
    public PageResponse<PropertyResponse> listApproved(Pageable pageable) {
        Page<Property> page = propertyRepository.findByStatus(ModerationStatus.APPROVED, pageable);
        return PageResponse.of(page, PropertyResponse::from);
    }

    @Transactional(readOnly = true)
    public List<PropertyResponse> findRecommendedProperties(List<Long> ids, int limit) {
        List<Property> properties = propertyRepository.findAllById(ids);
        return properties.stream()
                .filter(p -> p.getStatus() == ModerationStatus.APPROVED)
                .map(PropertyResponse::from)
                .limit(limit)
                .toList();
    }

    @Transactional(readOnly = true)
    public List<PropertyResponse> latestApproved(int limit) {
        PropertySearchCriteria criteria = new PropertySearchCriteria(null, null, null, null,
                null, null, null, null,
                PageRequest.of(0, limit, Sort.by(Sort.Direction.DESC, "createdAt")));
        return propertyRepository.findAll(PropertySpecifications.filter(criteria), criteria.pageable())
                .map(PropertyResponse::from)
                .getContent();
    }

    @Transactional(readOnly = true)
    public Property findProperty(Long id) {
        return propertyRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Property not found with id: " + id));
    }

    @Transactional(readOnly = true)
    public List<Room> findRooms(Long propertyId) {
        return roomRepository.findByPropertyId(propertyId);
    }

    @Transactional(readOnly = true)
    public boolean isOwnerOrAdmin(Property property) {
        try {
            User current = SecurityUtils.currentUser();
            return current.getRole() == com.staymart.entity.enums.Role.ADMIN
                    || current.getId().equals(property.getPostedBy().getId());
        } catch (Exception ex) {
            return false;
        }
    }
}