package com.voiceflow.javabackend.order;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "orders")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "order_number", nullable = false, unique = true, length = 50)
    private String orderNumber;

    @Column(name = "company_id")
    private UUID companyId;

    @Column(name = "customer_id")
    private UUID customerId;

    @Column(length = 200)
    private String item;

    @Column(length = 50)
    @Builder.Default
    private String status = "Processing";

    @Column(name = "expected_date", length = 50)
    private String expectedDate;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    public void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
