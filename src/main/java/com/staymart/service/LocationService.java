package com.staymart.service;

import com.staymart.dto.request.LocationRequest;
import com.staymart.dto.response.LocationResponse;
import com.staymart.entity.Location;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.LocationRepository;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class LocationService {

    private final LocationRepository locationRepository;

    public LocationService(LocationRepository locationRepository) {
        this.locationRepository = locationRepository;
    }

    @Transactional(readOnly = true)
    public List<LocationResponse> findAll() {
        return locationRepository.findAll().stream().map(LocationResponse::from).toList();
    }

    @Transactional(readOnly = true)
    public List<LocationResponse> findByCity(String city) {
        return locationRepository.findByCityIgnoreCase(city).stream().map(LocationResponse::from).toList();
    }

    @Transactional(readOnly = true)
    public List<LocationResponse> search(String query) {
        return locationRepository.findByCityContainingIgnoreCaseOrAreaContainingIgnoreCase(query, query)
                .stream().map(LocationResponse::from).toList();
    }

    @Transactional(readOnly = true)
    public List<String> listCities() {
        return locationRepository.findDistinctCities();
    }

    @Transactional
    public LocationResponse create(LocationRequest request) {
        Location location = Location.builder()
                .city(request.city().trim())
                .area(request.area())
                .state(request.state() == null || request.state().isBlank() ? "Uttarakhand" : request.state().trim())
                .pincode(request.pincode())
                .latitude(request.latitude())
                .longitude(request.longitude())
                .build();
        return LocationResponse.from(locationRepository.save(location));
    }

    @Transactional
    public LocationResponse update(Long id, LocationRequest request) {
        Location location = locationRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Location not found with id: " + id));
        location.setCity(request.city().trim());
        location.setArea(request.area());
        if (request.state() != null && !request.state().isBlank()) {
            location.setState(request.state().trim());
        }
        location.setPincode(request.pincode());
        location.setLatitude(request.latitude());
        location.setLongitude(request.longitude());
        return LocationResponse.from(locationRepository.save(location));
    }

    @Transactional
    public void delete(Long id) {
        Location location = locationRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Location not found with id: " + id));
        try {
            locationRepository.delete(location);
        } catch (DataIntegrityViolationException ex) {
            throw new BadRequestException("This location is in use by existing listings and cannot be deleted");
        }
    }
}