package com.voiceflow.javabackend.conversation.mapper;

import com.voiceflow.javabackend.common.enums.ConversationChannel;
import com.voiceflow.javabackend.common.enums.ConversationStatus;
import com.voiceflow.javabackend.conversation.dto.ConversationCreateRequest;
import com.voiceflow.javabackend.conversation.dto.ConversationResponse;
import com.voiceflow.javabackend.conversation.dto.MessageResponse;
import com.voiceflow.javabackend.conversation.entity.Conversation;
import com.voiceflow.javabackend.conversation.entity.Message;
import org.springframework.stereotype.Component;

@Component
public class ConversationMapper {

    public Conversation toEntity(ConversationCreateRequest request) {
        return Conversation.builder()
                .companyId(request.companyId())
                .customerId(request.customerId())
                .channel(request.channel() != null ? request.channel() : ConversationChannel.VOICE)
                .status(ConversationStatus.ACTIVE)
                .build();
    }

    public ConversationResponse toResponse(Conversation c) {
        return new ConversationResponse(
                c.getId(),
                c.getCompanyId(),
                c.getCustomerId(),
                c.getChannel(),
                c.getStatus(),
                c.getDetectedIntent(),
                c.getLastConfidence(),
                c.getStartedAt(),
                c.getEndedAt()
        );
    }

    public MessageResponse toMessageResponse(Message m) {
        return new MessageResponse(
                m.getId(),
                m.getConversationId(),
                m.getSender(),
                m.getContent(),
                m.getIntent(),
                m.getConfidence(),
                m.isEscalated(),
                m.getTicketId(),
                m.getBookingId(),
                m.getCreatedAt()
        );
    }
}
