package com.voiceflow.javabackend.conversation.controller;

import com.voiceflow.javabackend.conversation.dto.ConversationCreateRequest;
import com.voiceflow.javabackend.conversation.dto.ConversationResponse;
import com.voiceflow.javabackend.conversation.dto.MessageRequest;
import com.voiceflow.javabackend.conversation.dto.MessageResponse;
import com.voiceflow.javabackend.conversation.service.ConversationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/conversations")
@RequiredArgsConstructor
public class ConversationController {

    private final ConversationService conversationService;

    @PostMapping
    public ResponseEntity<ConversationResponse> createConversation(@RequestBody ConversationCreateRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(conversationService.createConversation(request));
    }

    @GetMapping
    public ResponseEntity<List<ConversationResponse>> getConversations(@RequestParam(required = false) UUID companyId) {
        return ResponseEntity.ok(conversationService.getConversations(companyId));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ConversationResponse> getConversationById(@PathVariable UUID id) {
        return ResponseEntity.ok(conversationService.getConversationById(id));
    }

    @PostMapping("/{id}/messages")
    public ResponseEntity<MessageResponse> sendMessage(
            @PathVariable UUID id,
            @Valid @RequestBody MessageRequest request
    ) {
        return ResponseEntity.ok(conversationService.sendMessage(id, request));
    }

    @GetMapping("/{id}/messages")
    public ResponseEntity<List<MessageResponse>> getMessages(@PathVariable UUID id) {
        return ResponseEntity.ok(conversationService.getMessages(id));
    }

    @PatchMapping("/{id}/end")
    public ResponseEntity<ConversationResponse> endConversation(@PathVariable UUID id) {
        return ResponseEntity.ok(conversationService.endConversation(id));
    }
}
