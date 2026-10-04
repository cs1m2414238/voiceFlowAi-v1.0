package com.voiceflow.javabackend.conversation.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "messages")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "conversation_id", nullable = false)
    private UUID conversationId;

    @Column(nullable = false, length = 30)
    private String sender;

    @Column(nullable = false, length = 4000)
    private String content;

    @Column(length = 80)
    private String intent;

    private Double confidence;

    private boolean escalated;

    @Column(name = "ticket_id", length = 60)
    private String ticketId;

    @Column(name = "booking_id", length = 60)
    private String bookingId;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    public void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
