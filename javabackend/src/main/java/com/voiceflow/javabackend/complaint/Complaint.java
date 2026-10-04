package com.voiceflow.javabackend.complaint;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "complaints")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Complaint {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "ticket_id", length = 50)
    private String ticketId;

    @Column(name = "company_id")
    private UUID companyId;

    @Column(length = 80)
    private String category;

    @Column(length = 1000)
    private String description;

    @Column(length = 40)
    @Builder.Default
    private String severity = "medium";

    @Column(length = 40)
    @Builder.Default
    private String status = "open";

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    public void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
