package com.voiceflow.javabackend.conversation.dto;

import com.voiceflow.javabackend.common.enums.ConversationChannel;

import java.util.UUID;

public record ConversationCreateRequest(
        UUID companyId,
        UUID customerId,
        ConversationChannel channel
) {
}
