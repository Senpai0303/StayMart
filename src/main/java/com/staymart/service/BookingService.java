package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.BookingRequest;
import com.staymart.dto.response.BookingResponse;
import com.staymart.entity.Booking;
import com.staymart.entity.Property;
import com.staymart.entity.Room;
import com.staymart.entity.User;
import com.staymart.entity.enums.BehaviorAction;
import com.staymart.entity.enums.BehaviorItemType;
import com.staymart.entity.enums.BookingStatus;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.exception.AccessForbiddenException;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.BookingRepository;
import com.staymart.util.SecurityUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;

@Service
public class BookingService {

    private final BookingRepository bookingRepository;
    private final PropertyService propertyService;
    private final RoomService roomService;
    private final BehaviorService behaviorService;

    public BookingService(BookingRepository bookingRepository,
                          PropertyService propertyService,
                          RoomService roomService,
                          BehaviorService behaviorService) {
        this.bookingRepository = bookingRepository;
        this.propertyService = propertyService;
        this.roomService = roomService;
        this.behaviorService = behaviorService;
    }

    @Transactional
    public BookingResponse create(BookingRequest request) {
        User booker = SecurityUtils.currentUser();
        Property property = propertyService.findProperty(request.propertyId());

        if (property.getStatus() != ModerationStatus.APPROVED) {
            throw new BadRequestException("This property is not available for booking yet");
        }
        if (booker.getId().equals(property.getPostedBy().getId())) {
            throw new BadRequestException("You cannot book your own property");
        }
        if (!Boolean.TRUE.equals(property.getIsAvailable())) {
            throw new BadRequestException("This property is currently unavailable");
        }

        Room room = null;
        if (request.roomId() != null) {
            room = roomService.findRoom(request.roomId());
            if (!room.getProperty().getId().equals(property.getId())) {
                throw new BadRequestException("Room does not belong to the selected property");
            }
            if (!Boolean.TRUE.equals(room.getIsAvailable())) {
                throw new BadRequestException("The selected room is currently unavailable");
            }
        }

        if (request.checkOut() != null && !request.checkOut().isAfter(request.checkIn())) {
            throw new BadRequestException("Check-out date must be after check-in date");
        }

        int months = request.months() == null ? 1 : request.months();
        BigDecimal pricePerMonth = room != null && room.getPrice() != null
                ? room.getPrice()
                : property.getPricePerMonth();
        BigDecimal total = pricePerMonth == null
                ? BigDecimal.ZERO
                : pricePerMonth.multiply(BigDecimal.valueOf(months));

        Booking booking = Booking.builder()
                .booker(booker)
                .property(property)
                .room(room)
                .checkIn(request.checkIn())
                .checkOut(request.checkOut())
                .months(months)
                .totalAmount(total)
                .status(BookingStatus.PENDING)
                .message(request.message())
                .build();

        Booking saved = bookingRepository.save(booking);
        behaviorService.record(booker.getId(), BehaviorItemType.PROPERTY, property.getId(),
                BehaviorAction.BOOK, null, property.getArea());
        return BookingResponse.from(saved);
    }

    @Transactional
    public BookingResponse updateStatus(Long bookingId, BookingStatus status) {
        Booking booking = findBooking(bookingId);
        if (!isOwnerOrAdmin(booking) && !isBooker(booking)) {
            throw new AccessForbiddenException("You can only update your own booking requests");
        }
        if (booking.getStatus() == BookingStatus.CANCELLED || booking.getStatus() == BookingStatus.COMPLETED) {
            throw new BadRequestException("A " + booking.getStatus().name().toLowerCase() + " booking cannot be changed");
        }
        if (status == BookingStatus.PENDING) {
            throw new BadRequestException("Invalid status change");
        }

        booking.setStatus(status);

        if (status == BookingStatus.CONFIRMED) {
            Property property = booking.getProperty();
            if (property.getAvailableRooms() != null && property.getAvailableRooms() > 0) {
                property.setAvailableRooms(property.getAvailableRooms() - 1);
            }
            if (booking.getRoom() != null) {
                booking.getRoom().setIsAvailable(false);
            }
        }
        if (status == BookingStatus.CANCELLED) {
            Property property = booking.getProperty();
            if (property.getAvailableRooms() != null
                    && property.getTotalRooms() != null
                    && property.getAvailableRooms() < property.getTotalRooms()) {
                property.setAvailableRooms(property.getAvailableRooms() + 1);
            }
            if (booking.getRoom() != null) {
                booking.getRoom().setIsAvailable(true);
            }
        }

        return BookingResponse.from(bookingRepository.save(booking));
    }

    @Transactional(readOnly = true)
    public PageResponse<BookingResponse> getMyBookings(Pageable pageable) {
        Page<Booking> page = bookingRepository.findByBookerId(SecurityUtils.currentUserId(), pageable);
        return PageResponse.of(page, BookingResponse::from);
    }

    @Transactional(readOnly = true)
    public PageResponse<BookingResponse> getIncomingBookings(Pageable pageable) {
        Page<Booking> page = bookingRepository.findByPropertyPostedById(SecurityUtils.currentUserId(), pageable);
        return PageResponse.of(page, BookingResponse::from);
    }

    @Transactional(readOnly = true)
    public BookingResponse getById(Long bookingId) {
        Booking booking = findBooking(bookingId);
        if (!isOwnerOrAdmin(booking) && !isBooker(booking)) {
            throw new AccessForbiddenException("You can only view your own bookings");
        }
        return BookingResponse.from(booking);
    }

    @Transactional(readOnly = true)
    public Booking findBooking(Long bookingId) {
        return bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + bookingId));
    }

    private boolean isOwnerOrAdmin(Booking booking) {
        User current = SecurityUtils.currentUser();
        return current.getRole() == com.staymart.entity.enums.Role.ADMIN
                || current.getId().equals(booking.getProperty().getPostedBy().getId());
    }

    private boolean isBooker(Booking booking) {
        return SecurityUtils.currentUserId().equals(booking.getBooker().getId());
    }
}