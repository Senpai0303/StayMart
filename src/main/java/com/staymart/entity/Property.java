package com.staymart.entity;

import com.staymart.entity.enums.GenderPreference;
import com.staymart.entity.enums.ModerationStatus;
import com.staymart.entity.enums.PropertyType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "properties")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Property {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "posted_by", nullable = false)
    private User postedBy;

    @Column(nullable = false, length = 200)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private PropertyType type;

    @Enumerated(EnumType.STRING)
    @Column(name = "gender_preference")
    @Builder.Default
    private GenderPreference genderPreference = GenderPreference.ANY;

    @Column(length = 255)
    private String address;

    @Column(length = 100)
    private String area;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "location_id")
    private Location location;

    @Column(name = "price_per_month", precision = 10, scale = 2)
    private BigDecimal pricePerMonth;

    @Column(name = "deposit_amount", precision = 10, scale = 2)
    @Builder.Default
    private BigDecimal depositAmount = BigDecimal.ZERO;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "json")
    @Builder.Default
    private List<String> amenities = new ArrayList<>();

    @Column(name = "total_rooms")
    @Builder.Default
    private Integer totalRooms = 1;

    @Column(name = "available_rooms")
    @Builder.Default
    private Integer availableRooms = 1;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "json")
    @Builder.Default
    private List<String> images = new ArrayList<>();

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private ModerationStatus status = ModerationStatus.PENDING;

    @Column(name = "is_available", nullable = false)
    @Builder.Default
    private Boolean isAvailable = true;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    void onCreate() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }
}
