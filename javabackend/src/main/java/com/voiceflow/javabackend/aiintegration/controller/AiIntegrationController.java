package com.voiceflow.javabackend.aiintegration.controller;

import com.voiceflow.javabackend.aiintegration.dto.AiChatRequest;
import com.voiceflow.javabackend.aiintegration.dto.AiChatResponse;
import com.voiceflow.javabackend.aiintegration.service.AiIntegrationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;

@RestController
@RequiredArgsConstructor
public class AiIntegrationController {

    private final AiIntegrationService aiIntegrationService;

    @PostMapping("/api/agents/chat")
    public ResponseEntity<AiChatResponse> chatWithAgent(@Valid @RequestBody AiChatRequest request) {
        return ResponseEntity.ok(aiIntegrationService.chat(request));
    }

    @PostMapping("/api/agents/config")
    public ResponseEntity<Map<String, Object>> saveAgentConfig(@RequestBody Map<String, Object> config) {
        return ResponseEntity.ok(aiIntegrationService.saveAgentConfig(config));
    }

    @GetMapping("/api/agents/config")
    public ResponseEntity<Map<String, Object>> getAgentConfig() {
        return ResponseEntity.ok(aiIntegrationService.getAgentConfig());
    }

    @PostMapping(value = {"/api/rag/upload", "/api/documents/upload"}, consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<Map<String, Object>> uploadDocument(
            @RequestParam("file") MultipartFile file,
            @RequestParam(value = "companyId", required = false, defaultValue = "default") String companyId
    ) throws IOException {
        Map<String, Object> result = aiIntegrationService.uploadDocument(
                file.getBytes(),
                file.getOriginalFilename(),
                companyId
        );
        return ResponseEntity.ok(result);
    }
}
