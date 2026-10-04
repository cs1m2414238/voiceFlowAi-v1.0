package com.voiceflow.javabackend.aiintegration.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiChatResponse {

    private String answer;
    private String intent;
    private double confidence;
    private boolean escalated;

    @JsonProperty("ticket_id")
    private String ticketId;

    @JsonProperty("booking_id")
    private String bookingId;
}
