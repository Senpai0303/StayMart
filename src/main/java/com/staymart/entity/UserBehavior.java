package com.staymart.entity;

import com.staymart.entity.enums.BehaviorAction;
import com.staymart.entity.enums.BehaviorItemType;
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

import java.time.LocalDateTime;

@Entity
@Table(name = "user_behaviors")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserBehavior {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Enumerated(EnumType.STRING)
    @Column(name = "item_type", nullable = false)
    private BehaviorItemType itemType;

    @Column(name = "item_id", nullable = false)
    private Long itemId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private BehaviorAction action;

    @Column(name = "timestamp")
    private LocalDateTime timestamp;

    @Column(name = "search_query", length = 255)
    private String searchQuery;

    @Column(name = "city_filter", length = 100)
    private String cityFilter;

    @PrePersist
    void onCreate() {
        if (timestamp == null) {
            timestamp = LocalDateTime.now();
        }
    }
}
