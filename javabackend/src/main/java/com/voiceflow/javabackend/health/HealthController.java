package com.voiceflow.javabackend.health;

import com.voiceflow.javabackend.aiintegration.dto.AiHealthResponse;
import com.voiceflow.javabackend.aiintegration.service.AiIntegrationService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.Map;

@RestController
@RequestMapping("/api/health")
@RequiredArgsConstructor
public class HealthController {

    private final AiIntegrationService aiIntegrationService;

    @GetMapping
    public ResponseEntity<Map<String, Object>> health() {
        AiHealthResponse aiHealth = aiIntegrationService.checkHealth();
        return ResponseEntity.ok(Map.of(
                "status", "UP",
                "backend", "voiceflow-java-backend",
                "aiService", aiHealth,
                "timestamp", LocalDateTime.now().toString()
        ));
    }
}
