package com.voiceflow.java_backend;

import com.voiceflow.javabackend.JavaBackendApplication;
import com.voiceflow.javabackend.aiintegration.dto.AiChatRequest;
import com.voiceflow.javabackend.aiintegration.dto.AiChatResponse;
import com.voiceflow.javabackend.aiintegration.service.AiIntegrationService;
import com.voiceflow.javabackend.auth.dto.AuthRequest;
import com.voiceflow.javabackend.auth.dto.AuthResponse;
import com.voiceflow.javabackend.auth.dto.RegisterRequest;
import com.voiceflow.javabackend.auth.service.AuthService;
import com.voiceflow.javabackend.common.enums.ConversationChannel;
import com.voiceflow.javabackend.company.dto.CompanyCreateRequest;
import com.voiceflow.javabackend.company.dto.CompanyResponse;
import com.voiceflow.javabackend.company.enums.IndustryType;
import com.voiceflow.javabackend.company.service.CompanyService;
import com.voiceflow.javabackend.conversation.dto.ConversationCreateRequest;
import com.voiceflow.javabackend.conversation.dto.ConversationResponse;
import com.voiceflow.javabackend.conversation.dto.MessageRequest;
import com.voiceflow.javabackend.conversation.dto.MessageResponse;
import com.voiceflow.javabackend.conversation.service.ConversationService;
import com.voiceflow.javabackend.user.enums.UserRole;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(classes = JavaBackendApplication.class)
class JavaBackendApplicationTests {

    @Autowired
    private CompanyService companyService;

    @Autowired
    private AuthService authService;

    @Autowired
    private ConversationService conversationService;

    @Autowired
    private AiIntegrationService aiIntegrationService;

    @Test
    void contextLoadsAndEndToEndFlowWorks() {
        // 1. Create a company
        CompanyResponse company = companyService.createCompany(new CompanyCreateRequest(
                "help@acme.com",
                "Acme Hospitality",
                IndustryType.HOTEL,
                "+1-555-0100"
        ));
        assertNotNull(company.id());
        assertEquals("Acme Hospitality", company.name());
        assertEquals("+1-555-0100", company.supportPhone());
        assertEquals("help@acme.com", company.supportEmail());

        // 2. Register and login a user
        AuthResponse registered = authService.register(new RegisterRequest(
                "Alice Admin",
                "alice@acme.com",
                "password123",
                UserRole.COMPANY_ADMIN,
                company.id()
        ));
        assertNotNull(registered.token());

        AuthResponse loggedIn = authService.login(new AuthRequest("alice@acme.com", "password123"));
        assertNotNull(loggedIn.token());
        assertEquals(company.id(), loggedIn.companyId());

        // 3. Create a conversation and send a message through AI integration
        ConversationResponse conv = conversationService.createConversation(new ConversationCreateRequest(
                company.id(),
                null,
                ConversationChannel.CHAT
        ));
        assertNotNull(conv.id());

        MessageResponse reply = conversationService.sendMessage(conv.id(), new MessageRequest(
                "I want to book a table for Friday",
                "USER"
        ));
        assertNotNull(reply.id());
        assertEquals("AGENT", reply.sender());
        assertNotNull(reply.content());
        assertNotNull(reply.intent());

        // 4. Direct AI chat call
        AiChatResponse directChat = aiIntegrationService.chat(AiChatRequest.builder()
                .question("Where is my order 1001?")
                .companyId(company.id().toString())
                .sessionId("test-session")
                .build());
        assertNotNull(directChat.getAnswer());
    }
}
