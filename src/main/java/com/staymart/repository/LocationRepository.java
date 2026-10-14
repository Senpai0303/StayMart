package com.staymart.repository;

import com.staymart.entity.Location;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface LocationRepository extends JpaRepository<Location, Long> {

    List<Location> findByCityIgnoreCase(String city);

    List<Location> findByCityContainingIgnoreCaseOrAreaContainingIgnoreCase(String city, String area);

    @Query("SELECT DISTINCT l.city FROM Location l ORDER BY l.city")
    List<String> findDistinctCities();
}