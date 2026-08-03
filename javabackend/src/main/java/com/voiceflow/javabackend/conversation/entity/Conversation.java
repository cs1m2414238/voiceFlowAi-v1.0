package com.voiceflow.javabackend.conversation.entity;

import com.voiceflow.javabackend.common.enums.ConversationChannel;
import com.voiceflow.javabackend.common.enums.ConversationStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Conversation {
    private UUID id;
    private UUID companyId;
    private UUID customerId;
    private ConversationChannel channel;
    private ConversationStatus status;
    private String detectedIntent;
    private Double lastConfidence;
    private LocalDateTime startedAt;
    private LocalDateTime endedAt;
}
