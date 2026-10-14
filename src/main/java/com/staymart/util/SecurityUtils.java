package com.staymart.util;

import com.staymart.entity.User;
import com.staymart.exception.AccessForbiddenException;
import com.staymart.security.SecurityUser;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

public final class SecurityUtils {

    private SecurityUtils() {
    }

    public static User currentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof SecurityUser securityUser)) {
            throw new AccessForbiddenException("You must be logged in to perform this action");
        }
        return securityUser.getUser();
    }

    public static Long currentUserId() {
        return currentUser().getId();
    }

    public static Long currentUserIdOrNull() {
        try {
            return currentUserId();
        } catch (Exception ex) {
            return null;
        }
    }

    public static boolean isAdmin() {
        return currentUser().getRole() == com.staymart.entity.enums.Role.ADMIN;
    }
}