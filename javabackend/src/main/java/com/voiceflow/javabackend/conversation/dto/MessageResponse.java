package com.voiceflow.javabackend.conversation.dto;

import java.time.LocalDateTime;
import java.util.UUID;

public record MessageResponse(
        UUID id,
        UUID conversationId,
        String sender,
        String content,
        String intent,
        Double confidence,
        boolean escalated,
        String ticketId,
        String bookingId,
        LocalDateTime createdAt
) {
}
