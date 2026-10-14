package com.staymart.repository;

import com.staymart.entity.Booking;
import com.staymart.entity.enums.BookingStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BookingRepository extends JpaRepository<Booking, Long> {

    Page<Booking> findByBookerId(Long bookerId, Pageable pageable);

    Page<Booking> findByPropertyPostedById(Long ownerId, Pageable pageable);

    List<Booking> findByPropertyIdAndStatus(Long propertyId, BookingStatus status);

    long countByStatus(BookingStatus status);
}