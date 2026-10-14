package com.staymart.repository;

import com.staymart.entity.User;
import com.staymart.entity.enums.Role;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);

    long countByRole(Role role);

    Page<User> findByRole(Role role, Pageable pageable);

    @Query("SELECT COALESCE(u.city, 'Unknown'), COUNT(u) FROM User u GROUP BY u.city ORDER BY COUNT(u) DESC")
    List<Object[]> countGroupByCity();

    @Query("SELECT YEAR(u.createdAt), MONTH(u.createdAt), COUNT(u) FROM User u "
            + "WHERE u.createdAt >= :since GROUP BY YEAR(u.createdAt), MONTH(u.createdAt) "
            + "ORDER BY YEAR(u.createdAt), MONTH(u.createdAt)")
    List<Object[]> countCreatedByMonthSince(@Param("since") LocalDateTime since);
}