package com.voiceflow.javabackend.conversation.dto;

import com.voiceflow.javabackend.common.enums.ConversationChannel;
import com.voiceflow.javabackend.common.enums.ConversationStatus;

import java.time.LocalDateTime;
import java.util.UUID;

public record ConversationResponse(
        UUID id,
        UUID companyId,
        UUID customerId,
        ConversationChannel channel,
        ConversationStatus status,
        String detectedIntent,
        Double lastConfidence,
        LocalDateTime startedAt,
        LocalDateTime endedAt
) {
}
