package com.voiceflow.javabackend.aiintegration.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
@Getter
@Setter
public class AiServiceProperties {

    @Value("${ai.service.base-url:http://localhost:8000}")
    private String baseUrl;

    @Value("${ai.service.timeout-seconds:30}")
    private int timeoutSeconds;

    @Bean
    public RestTemplate aiRestTemplate() {
        return new RestTemplate();
    }
}
