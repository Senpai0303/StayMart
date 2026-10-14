package com.staymart.service;

import com.staymart.dto.request.LoginRequest;
import com.staymart.dto.request.RegisterRequest;
import com.staymart.dto.response.AuthResponse;
import com.staymart.dto.response.UserResponse;
import com.staymart.entity.User;
import com.staymart.entity.enums.Role;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.DuplicateResourceException;
import com.staymart.repository.UserRepository;
import com.staymart.security.JwtService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final long jwtExpirationMs;

    public AuthService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       AuthenticationManager authenticationManager,
                       JwtService jwtService,
                       @Value("${app.jwt.expiration-ms}") long jwtExpirationMs) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.jwtService = jwtService;
        this.jwtExpirationMs = jwtExpirationMs;
    }

    @Transactional
    public AuthResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.email().trim().toLowerCase())) {
            throw new DuplicateResourceException("An account already exists with email: " + request.email());
        }

        User user = User.builder()
                .name(request.name().trim())
                .email(request.email().trim().toLowerCase())
                .passwordHash(passwordEncoder.encode(request.password()))
                .phone(request.phone())
                .role(Role.USER)
                .city(request.city() == null || request.city().isBlank() ? "Dehradun" : request.city().trim())
                .state(request.state() == null || request.state().isBlank() ? "Uttarakhand" : request.state().trim())
                .isActive(true)
                .isVerified(false)
                .build();

        User saved = userRepository.save(user);
        return AuthResponse.of(jwtService.generateToken(saved), jwtExpirationMs, saved);
    }

    @Transactional(readOnly = true)
    public AuthResponse login(LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.email().trim().toLowerCase(), request.password())
        );

        User user = userRepository.findByEmail(authentication.getName())
                .orElseThrow(() -> new BadRequestException("Invalid email or password"));

        if (!Boolean.TRUE.equals(user.getIsActive())) {
            throw new BadRequestException("Your account has been deactivated. Contact support.");
        }

        return AuthResponse.of(jwtService.generateToken(user), jwtExpirationMs, user);
    }

    @Transactional(readOnly = true)
    public UserResponse me() {
        return UserResponse.from(com.staymart.util.SecurityUtils.currentUser());
    }
}