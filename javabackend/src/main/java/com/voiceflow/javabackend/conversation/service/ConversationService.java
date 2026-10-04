package com.voiceflow.javabackend.conversation.service;

import com.voiceflow.javabackend.conversation.dto.ConversationCreateRequest;
import com.voiceflow.javabackend.conversation.dto.ConversationResponse;
import com.voiceflow.javabackend.conversation.dto.MessageRequest;
import com.voiceflow.javabackend.conversation.dto.MessageResponse;

import java.util.List;
import java.util.UUID;

public interface ConversationService {
    ConversationResponse createConversation(ConversationCreateRequest request);
    ConversationResponse getConversationById(UUID id);
    List<ConversationResponse> getConversations(UUID companyId);
    MessageResponse sendMessage(UUID conversationId, MessageRequest request);
    List<MessageResponse> getMessages(UUID conversationId);
    ConversationResponse endConversation(UUID id);
}
