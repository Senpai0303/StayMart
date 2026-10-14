package com.staymart.repository;

import com.staymart.entity.Room;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RoomRepository extends JpaRepository<Room, Long> {

    List<Room> findByPropertyId(Long propertyId);

    long countByPropertyId(Long propertyId);
}