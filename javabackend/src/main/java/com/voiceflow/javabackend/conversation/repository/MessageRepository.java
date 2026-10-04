package com.voiceflow.javabackend.conversation.repository;

import com.voiceflow.javabackend.conversation.entity.Message;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface MessageRepository extends JpaRepository<Message, UUID> {
    List<Message> findByConversationIdOrderByCreatedAtAsc(UUID conversationId);
}
