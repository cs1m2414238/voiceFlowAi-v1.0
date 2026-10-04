package com.voiceflow.javabackend.notification;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
@Slf4j
public class NotificationService {

    public void notifyEscalation(UUID companyId, UUID conversationId, String reason) {
        log.info("Escalation notification dispatched for company={} conversation={}: {}",
                companyId, conversationId, reason);
    }
}
