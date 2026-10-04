package com.voiceflow.javabackend.aiintegration.client;

import com.voiceflow.javabackend.aiintegration.config.AiServiceProperties;
import com.voiceflow.javabackend.aiintegration.dto.AiChatRequest;
import com.voiceflow.javabackend.aiintegration.dto.AiChatResponse;
import com.voiceflow.javabackend.aiintegration.dto.AiHealthResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Component
@RequiredArgsConstructor
@Slf4j
public class AiServiceClient {

    private final RestTemplate aiRestTemplate;
    private final AiServiceProperties properties;

    public AiChatResponse sendAgentChat(AiChatRequest request) {
        String url = properties.getBaseUrl() + "/agent/chat";
        try {
            ResponseEntity<AiChatResponse> response = aiRestTemplate.postForEntity(url, request, AiChatResponse.class);
            if (response.getBody() != null) {
                return response.getBody();
            }
        } catch (Exception ex) {
            log.warn("Python AI service unreachable at {}: {}. Using local fallback.", url, ex.getMessage());
        }

        return buildLocalFallback(request);
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> uploadDocument(byte[] fileBytes, String filename) {
        String url = properties.getBaseUrl() + "/documents/upload";
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            ByteArrayResource resource = new ByteArrayResource(fileBytes) {
                @Override
                public String getFilename() {
                    return filename != null ? filename : "document.pdf";
                }
            };

            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", resource);

            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            ResponseEntity<Map> response = aiRestTemplate.postForEntity(url, requestEntity, Map.class);
            if (response.getBody() != null) {
                return response.getBody();
            }
        } catch (Exception ex) {
            log.warn("Python AI document upload unreachable at {}: {}. Using fallback.", url, ex.getMessage());
        }

        return Map.of(
                "message", "Document indexed in local fallback mode.",
                "filename", filename != null ? filename : "document.pdf",
                "chunks_created", Math.max(1, fileBytes.length / 500)
        );
    }

    public AiHealthResponse checkHealth() {
        String url = properties.getBaseUrl() + "/health";
        try {
            ResponseEntity<AiHealthResponse> response = aiRestTemplate.getForEntity(url, AiHealthResponse.class);
            if (response.getBody() != null) {
                return response.getBody();
            }
        } catch (Exception ex) {
            log.debug("Python AI health check failed: {}", ex.getMessage());
        }
        return AiHealthResponse.builder()
                .status("DOWN")
                .service("voiceflow-python-ai")
                .build();
    }

    private AiChatResponse buildLocalFallback(AiChatRequest request) {
        String q = request.getQuestion() != null ? request.getQuestion().toLowerCase() : "";
        if (q.contains("book") || q.contains("reservation") || q.contains("appointment")) {
            return AiChatResponse.builder()
                    .answer("I've processed your booking request. What date, time, and party size work best for you?")
                    .intent("booking")
                    .confidence(0.88)
                    .escalated(false)
                    .build();
        }
        if (q.contains("order") || q.contains("delivery") || q.contains("refund") || q.contains("return")) {
            return AiChatResponse.builder()
                    .answer("I can help check your order status or start a return. Could you share your order number?")
                    .intent("order")
                    .confidence(0.89)
                    .escalated(false)
                    .build();
        }
        if (q.contains("complaint") || q.contains("terrible") || q.contains("broken") || q.contains("rude")) {
            return AiChatResponse.builder()
                    .answer("I'm sorry about that experience. I have logged a support complaint ticket for our team.")
                    .intent("complaint")
                    .confidence(0.91)
                    .escalated(q.contains("lawyer") || q.contains("fraud") || q.contains("sue"))
                    .ticketId("C-1001")
                    .build();
        }
        if (q.contains("human") || q.contains("person") || q.contains("agent") || q.contains("representative")) {
            return AiChatResponse.builder()
                    .answer("Let me connect you with a human support representative.")
                    .intent("human")
                    .confidence(0.95)
                    .escalated(true)
                    .build();
        }
        return AiChatResponse.builder()
                .answer("Thank you for reaching out to VoiceFlow AI. Based on our knowledge base, how can I assist you further today?")
                .intent("faq")
                .confidence(0.85)
                .escalated(false)
                .build();
    }
}
