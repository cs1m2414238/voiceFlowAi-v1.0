package com.voiceflow.javabackend.aiintegration.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiChatRequest {

    @NotBlank(message = "Question is required")
    private String question;

    @JsonProperty("company_id")
    @Builder.Default
    private String companyId = "default";

    @JsonProperty("session_id")
    @Builder.Default
    private String sessionId = "default";
}
