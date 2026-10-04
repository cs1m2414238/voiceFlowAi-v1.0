package com.voiceflow.javabackend.aiintegration.service;

import com.voiceflow.javabackend.aiintegration.dto.AiChatRequest;
import com.voiceflow.javabackend.aiintegration.dto.AiChatResponse;
import com.voiceflow.javabackend.aiintegration.dto.AiHealthResponse;

import java.util.Map;

public interface AiIntegrationService {

    AiChatResponse chat(AiChatRequest request);

    Map<String, Object> uploadDocument(byte[] fileBytes, String filename, String companyId);

    AiHealthResponse checkHealth();

    Map<String, Object> saveAgentConfig(Map<String, Object> config);

    Map<String, Object> getAgentConfig();
}
