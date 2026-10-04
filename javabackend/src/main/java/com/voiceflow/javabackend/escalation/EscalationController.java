package com.voiceflow.javabackend.escalation;

import com.voiceflow.javabackend.common.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/escalations")
@RequiredArgsConstructor
public class EscalationController {

    private final EscalationRepository escalationRepository;

    @PostMapping
    public ResponseEntity<Escalation> createEscalation(@RequestBody Escalation escalation) {
        return ResponseEntity.status(HttpStatus.CREATED).body(escalationRepository.save(escalation));
    }

    @GetMapping
    public ResponseEntity<List<Escalation>> getEscalations(@RequestParam(required = false) UUID companyId) {
        List<Escalation> list = companyId != null
                ? escalationRepository.findByCompanyId(companyId)
                : escalationRepository.findAll();
        return ResponseEntity.ok(list);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Escalation> getEscalationById(@PathVariable UUID id) {
        Escalation esc = escalationRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Escalation", id));
        return ResponseEntity.ok(esc);
    }

    @PatchMapping("/{id}/resolve")
    public ResponseEntity<Escalation> resolveEscalation(
            @PathVariable UUID id,
            @RequestBody(required = false) Map<String, String> body
    ) {
        Escalation esc = escalationRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Escalation", id));
        esc.setStatus("RESOLVED");
        esc.setResolvedAt(LocalDateTime.now());
        if (body != null && body.containsKey("assignedAgent")) {
            esc.setAssignedAgent(body.get("assignedAgent"));
        }
        return ResponseEntity.ok(escalationRepository.save(esc));
    }
}
