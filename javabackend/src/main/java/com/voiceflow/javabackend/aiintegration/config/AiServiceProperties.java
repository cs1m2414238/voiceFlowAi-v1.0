package com.voiceflow.javabackend.aiintegration.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Configuration
@Getter
@Setter
public class AiServiceProperties {

    @Value("${ai.service.base-url:http://localhost:8000}")
    private String baseUrl;

    @Value("${ai.service.timeout-seconds:120}")
    private int timeoutSeconds;

    @Value("${ai.local-fallback.enabled:false}")
    private boolean localFallbackEnabled;

    @Bean
    public RestTemplate aiRestTemplate() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        Duration timeout = Duration.ofSeconds(Math.max(1, timeoutSeconds));
        factory.setConnectTimeout(timeout);
        factory.setReadTimeout(timeout);
        return new RestTemplate(factory);
    }
}
