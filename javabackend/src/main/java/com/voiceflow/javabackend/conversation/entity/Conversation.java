package com.voiceflow.javabackend.conversation.entity;

import com.voiceflow.javabackend.common.enums.ConversationChannel;
import com.voiceflow.javabackend.common.enums.ConversationStatus;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "conversations")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Conversation {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "company_id")
    private UUID companyId;

    @Column(name = "customer_id")
    private UUID customerId;

    @Enumerated(EnumType.STRING)
    @Builder.Default
    @Column(nullable = false)
    private ConversationChannel channel = ConversationChannel.VOICE;

    @Enumerated(EnumType.STRING)
    @Builder.Default
    @Column(nullable = false)
    private ConversationStatus status = ConversationStatus.ACTIVE;

    @Column(name = "detected_intent", length = 80)
    private String detectedIntent;

    @Column(name = "last_confidence")
    private Double lastConfidence;

    @Column(name = "started_at", nullable = false, updatable = false)
    private LocalDateTime startedAt;

    @Column(name = "ended_at")
    private LocalDateTime endedAt;

    @PrePersist
    public void onCreate() {
        if (startedAt == null) {
            startedAt = LocalDateTime.now();
        }
        if (channel == null) {
            channel = ConversationChannel.VOICE;
        }
        if (status == null) {
            status = ConversationStatus.ACTIVE;
        }
    }
}
