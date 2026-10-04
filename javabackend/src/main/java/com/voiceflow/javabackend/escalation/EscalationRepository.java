package com.voiceflow.javabackend.escalation;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface EscalationRepository extends JpaRepository<Escalation, UUID> {
    List<Escalation> findByCompanyId(UUID companyId);
    List<Escalation> findByStatus(String status);
}
