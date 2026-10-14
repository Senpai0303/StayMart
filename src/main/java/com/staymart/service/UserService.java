package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.ChangePasswordRequest;
import com.staymart.dto.request.UpdateProfileRequest;
import com.staymart.dto.response.PropertyResponse;
import com.staymart.dto.response.ProductResponse;
import com.staymart.dto.response.UserResponse;
import com.staymart.dto.response.UserSummary;
import com.staymart.entity.Property;
import com.staymart.entity.Product;
import com.staymart.entity.User;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.PropertyRepository;
import com.staymart.repository.ProductRepository;
import com.staymart.repository.UserRepository;
import com.staymart.util.SecurityUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PropertyRepository propertyRepository;
    private final ProductRepository productRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository,
                       PropertyRepository propertyRepository,
                       ProductRepository productRepository,
                       PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.propertyRepository = propertyRepository;
        this.productRepository = productRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional(readOnly = true)
    public UserResponse getMyProfile() {
        return UserResponse.from(SecurityUtils.currentUser());
    }

    @Transactional
    public UserResponse updateMyProfile(UpdateProfileRequest request) {
        User user = SecurityUtils.currentUser();
        if (request.name() != null && !request.name().isBlank()) {
            user.setName(request.name().trim());
        }
        if (request.phone() != null) {
            user.setPhone(request.phone());
        }
        if (request.profilePic() != null) {
            user.setProfilePic(request.profilePic());
        }
        if (request.city() != null && !request.city().isBlank()) {
            user.setCity(request.city().trim());
        }
        if (request.state() != null && !request.state().isBlank()) {
            user.setState(request.state().trim());
        }
        if (request.bio() != null) {
            user.setBio(request.bio());
        }
        return UserResponse.from(userRepository.save(user));
    }

    @Transactional
    public void changePassword(ChangePasswordRequest request) {
        User user = SecurityUtils.currentUser();
        if (!passwordEncoder.matches(request.currentPassword(), user.getPasswordHash())) {
            throw new BadRequestException("Current password is incorrect");
        }
        if (passwordEncoder.matches(request.newPassword(), user.getPasswordHash())) {
            throw new BadRequestException("New password must be different from the current password");
        }
        user.setPasswordHash(passwordEncoder.encode(request.newPassword()));
        userRepository.save(user);
    }

    @Transactional(readOnly = true)
    public UserSummary getUserSummary(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));
        return UserSummary.from(user);
    }

    @Transactional(readOnly = true)
    public UserResponse getUserProfile(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));
        return UserResponse.from(user);
    }

    @Transactional(readOnly = true)
    public PageResponse<PropertyResponse> getMyProperties(Pageable pageable) {
        Long userId = SecurityUtils.currentUserId();
        Page<Property> page = propertyRepository.findByPostedById(userId, pageable);
        return PageResponse.of(page, PropertyResponse::from);
    }

    @Transactional(readOnly = true)
    public PageResponse<ProductResponse> getMyProducts(Pageable pageable) {
        Long userId = SecurityUtils.currentUserId();
        Page<Product> page = productRepository.findByPostedById(userId, pageable);
        return PageResponse.of(page, ProductResponse::from);
    }

    @Transactional(readOnly = true)
    public PageResponse<PropertyResponse> getPropertiesByUser(Long userId, Pageable pageable) {
        Page<Property> page = propertyRepository.findByPostedById(userId, pageable);
        return PageResponse.of(page, PropertyResponse::from);
    }
}