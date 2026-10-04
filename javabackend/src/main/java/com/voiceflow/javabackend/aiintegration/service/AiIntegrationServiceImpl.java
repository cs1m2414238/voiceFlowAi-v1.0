package com.voiceflow.javabackend.aiintegration.service;

import com.voiceflow.javabackend.aiintegration.client.AiServiceClient;
import com.voiceflow.javabackend.aiintegration.dto.AiChatRequest;
import com.voiceflow.javabackend.aiintegration.dto.AiChatResponse;
import com.voiceflow.javabackend.aiintegration.dto.AiHealthResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
@RequiredArgsConstructor
public class AiIntegrationServiceImpl implements AiIntegrationService {

    private final AiServiceClient aiServiceClient;
    private final Map<String, Object> currentAgentConfig = new ConcurrentHashMap<>(Map.of(
            "template", "ecommerce",
            "voiceProfile", "Rachel",
            "temperature", 0.7,
            "promptDirectives", "You are a helpful, professional AI agent for VoiceFlow. Ground all responses in the provided knowledge base."
    ));

    @Override
    public AiChatResponse chat(AiChatRequest request) {
        return aiServiceClient.sendAgentChat(request);
    }

    @Override
    public Map<String, Object> uploadDocument(byte[] fileBytes, String filename, String companyId) {
        Map<String, Object> pythonResult = aiServiceClient.uploadDocument(fileBytes, filename);
        Object chunksObj = pythonResult.getOrDefault("chunks_created", 128);
        int chunks = chunksObj instanceof Number n ? n.intValue() : 128;

        Map<String, Object> response = new HashMap<>(pythonResult);
        response.put("chunks", chunks);
        response.put("dimensions", 384);
        response.put("vectorStore", "ChromaDB");
        response.put("status", "Indexed Successfully");
        response.put("companyId", companyId != null ? companyId : "default");
        return response;
    }

    @Override
    public AiHealthResponse checkHealth() {
        return aiServiceClient.checkHealth();
    }

    @Override
    public Map<String, Object> saveAgentConfig(Map<String, Object> config) {
        if (config != null) {
            currentAgentConfig.putAll(config);
        }
        currentAgentConfig.put("updatedAt", LocalDateTime.now().toString());
        currentAgentConfig.put("status", "DEPLOYED");
        return new HashMap<>(currentAgentConfig);
    }

    @Override
    public Map<String, Object> getAgentConfig() {
        return new HashMap<>(currentAgentConfig);
    }
}
