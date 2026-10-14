package com.staymart.entity;

import com.staymart.entity.enums.RoomType;
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
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "rooms")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Room {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "property_id", nullable = false)
    private Property property;

    @Column(name = "room_number", length = 20)
    private String roomNumber;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private RoomType type;

    @Column(precision = 10, scale = 2)
    private BigDecimal price;

    @Builder.Default
    private Integer capacity = 1;

    @Column(name = "floor_number")
    @Builder.Default
    private Integer floorNumber = 0;

    @Column(name = "is_available", nullable = false)
    @Builder.Default
    private Boolean isAvailable = true;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "json")
    @Builder.Default
    private List<String> images = new ArrayList<>();
}
