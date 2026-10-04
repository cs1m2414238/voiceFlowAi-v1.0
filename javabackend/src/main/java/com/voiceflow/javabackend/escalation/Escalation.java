package com.voiceflow.javabackend.escalation;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "escalations")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Escalation {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "company_id")
    private UUID companyId;

    @Column(name = "conversation_id")
    private UUID conversationId;

    @Column(name = "ticket_id")
    private String ticketId;

    @Column(length = 500)
    private String reason;

    @Column(length = 50)
    @Builder.Default
    private String priority = "HIGH";

    @Column(length = 50)
    @Builder.Default
    private String status = "OPEN";

    @Column(length = 120)
    private String assignedAgent;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    private LocalDateTime resolvedAt;

    @PrePersist
    public void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
