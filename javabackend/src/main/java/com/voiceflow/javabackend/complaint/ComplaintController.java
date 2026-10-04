package com.voiceflow.javabackend.complaint;

import com.voiceflow.javabackend.common.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/complaints")
@RequiredArgsConstructor
public class ComplaintController {

    private final ComplaintRepository complaintRepository;

    @PostMapping
    public ResponseEntity<Complaint> createComplaint(@RequestBody Complaint complaint) {
        return ResponseEntity.status(HttpStatus.CREATED).body(complaintRepository.save(complaint));
    }

    @GetMapping
    public ResponseEntity<List<Complaint>> getComplaints(@RequestParam(required = false) UUID companyId) {
        List<Complaint> list = companyId != null
                ? complaintRepository.findByCompanyId(companyId)
                : complaintRepository.findAll();
        return ResponseEntity.ok(list);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Complaint> getComplaintById(@PathVariable UUID id) {
        return ResponseEntity.ok(complaintRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Complaint", id)));
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<Complaint> updateComplaintStatus(
            @PathVariable UUID id,
            @RequestBody Map<String, String> body
    ) {
        Complaint complaint = complaintRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Complaint", id));
        if (body.containsKey("status")) {
            complaint.setStatus(body.get("status"));
        }
        return ResponseEntity.ok(complaintRepository.save(complaint));
    }
}
