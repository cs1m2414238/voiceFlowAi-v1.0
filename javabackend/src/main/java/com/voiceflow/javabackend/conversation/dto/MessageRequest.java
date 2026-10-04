package com.voiceflow.javabackend.conversation.dto;

import jakarta.validation.constraints.NotBlank;

public record MessageRequest(
        @NotBlank(message = "Message content is required")
        String content,
        String sender
) {
}
