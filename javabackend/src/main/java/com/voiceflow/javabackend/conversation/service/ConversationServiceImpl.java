package com.voiceflow.javabackend.conversation.service;

import com.voiceflow.javabackend.aiintegration.dto.AiChatRequest;
import com.voiceflow.javabackend.aiintegration.dto.AiChatResponse;
import com.voiceflow.javabackend.aiintegration.service.AiIntegrationService;
import com.voiceflow.javabackend.booking.Booking;
import com.voiceflow.javabackend.booking.BookingRepository;
import com.voiceflow.javabackend.booking.BookingStatus;
import com.voiceflow.javabackend.common.enums.ConversationStatus;
import com.voiceflow.javabackend.common.exception.ResourceNotFoundException;
import com.voiceflow.javabackend.complaint.Complaint;
import com.voiceflow.javabackend.complaint.ComplaintRepository;
import com.voiceflow.javabackend.conversation.dto.ConversationCreateRequest;
import com.voiceflow.javabackend.conversation.dto.ConversationResponse;
import com.voiceflow.javabackend.conversation.dto.MessageRequest;
import com.voiceflow.javabackend.conversation.dto.MessageResponse;
import com.voiceflow.javabackend.conversation.entity.Conversation;
import com.voiceflow.javabackend.conversation.entity.Message;
import com.voiceflow.javabackend.conversation.mapper.ConversationMapper;
import com.voiceflow.javabackend.conversation.repository.ConversationRepository;
import com.voiceflow.javabackend.conversation.repository.MessageRepository;
import com.voiceflow.javabackend.escalation.Escalation;
import com.voiceflow.javabackend.escalation.EscalationRepository;
import com.voiceflow.javabackend.notification.NotificationService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ConversationServiceImpl implements ConversationService {

    private final ConversationRepository conversationRepository;
    private final MessageRepository messageRepository;
    private final ConversationMapper conversationMapper;
    private final AiIntegrationService aiIntegrationService;
    private final EscalationRepository escalationRepository;
    private final ComplaintRepository complaintRepository;
    private final BookingRepository bookingRepository;
    private final NotificationService notificationService;

    @Override
    @Transactional
    public ConversationResponse createConversation(ConversationCreateRequest request) {
        Conversation conversation = conversationMapper.toEntity(request);
        return conversationMapper.toResponse(conversationRepository.save(conversation));
    }

    @Override
    public ConversationResponse getConversationById(UUID id) {
        Conversation conversation = conversationRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Conversation", id));
        return conversationMapper.toResponse(conversation);
    }

    @Override
    public List<ConversationResponse> getConversations(UUID companyId) {
        List<Conversation> list = companyId != null
                ? conversationRepository.findByCompanyIdOrderByStartedAtDesc(companyId)
                : conversationRepository.findAll();
        return list.stream().map(conversationMapper::toResponse).toList();
    }

    @Override
    @Transactional
    public MessageResponse sendMessage(UUID conversationId, MessageRequest request) {
        Conversation conversation = conversationRepository.findById(conversationId)
                .orElseThrow(() -> new ResourceNotFoundException("Conversation", conversationId));

        String sender = request.sender() != null && !request.sender().isBlank()
                ? request.sender().toUpperCase()
                : "USER";

        Message userMessage = Message.builder()
                .conversationId(conversationId)
                .sender(sender)
                .content(request.content())
                .build();
        messageRepository.save(userMessage);

        AiChatRequest aiRequest = AiChatRequest.builder()
                .question(request.content())
                .companyId(conversation.getCompanyId() != null ? conversation.getCompanyId().toString() : "default")
                .sessionId(conversationId.toString())
                .build();

        AiChatResponse aiResponse = aiIntegrationService.chat(aiRequest);

        conversation.setDetectedIntent(aiResponse.getIntent());
        conversation.setLastConfidence(aiResponse.getConfidence());
        if (aiResponse.isEscalated()) {
            String reason = "Escalated during " + aiResponse.getIntent() + " flow: " + request.content();
            conversation.setStatus(ConversationStatus.ESCALATED);
            escalationRepository.save(Escalation.builder()
                    .companyId(conversation.getCompanyId())
                    .conversationId(conversationId)
                    .ticketId(aiResponse.getTicketId())
                    .reason(reason)
                    .priority("HIGH")
                    .status("OPEN")
                    .build());
            notificationService.notifyEscalation(conversation.getCompanyId(), conversationId, reason);
        } else if (conversation.getStatus() == ConversationStatus.ACTIVE) {
            conversation.setStatus(ConversationStatus.IN_PROGRESS);
        }
        conversationRepository.save(conversation);

        if (aiResponse.getTicketId() != null) {
            complaintRepository.save(Complaint.builder()
                    .ticketId(aiResponse.getTicketId())
                    .companyId(conversation.getCompanyId())
                    .category("support")
                    .description(request.content())
                    .severity(aiResponse.isEscalated() ? "high" : "medium")
                    .status("open")
                    .build());
        }

        if (aiResponse.getBookingId() != null) {
            bookingRepository.save(Booking.builder()
                    .bookingReference(aiResponse.getBookingId())
                    .companyId(conversation.getCompanyId())
                    .customerId(conversation.getCustomerId())
                    .status(BookingStatus.CONFIRMED)
                    .build());
        }

        Message agentMessage = Message.builder()
                .conversationId(conversationId)
                .sender("AGENT")
                .content(aiResponse.getAnswer())
                .intent(aiResponse.getIntent())
                .confidence(aiResponse.getConfidence())
                .escalated(aiResponse.isEscalated())
                .ticketId(aiResponse.getTicketId())
                .bookingId(aiResponse.getBookingId())
                .build();

        return conversationMapper.toMessageResponse(messageRepository.save(agentMessage));
    }

    @Override
    public List<MessageResponse> getMessages(UUID conversationId) {
        if (!conversationRepository.existsById(conversationId)) {
            throw new ResourceNotFoundException("Conversation", conversationId);
        }
        return messageRepository.findByConversationIdOrderByCreatedAtAsc(conversationId)
                .stream()
                .map(conversationMapper::toMessageResponse)
                .toList();
    }

    @Override
    @Transactional
    public ConversationResponse endConversation(UUID id) {
        Conversation conversation = conversationRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Conversation", id));
        conversation.setStatus(ConversationStatus.COMPLETED);
        conversation.setEndedAt(LocalDateTime.now());
        return conversationMapper.toResponse(conversationRepository.save(conversation));
    }
}
