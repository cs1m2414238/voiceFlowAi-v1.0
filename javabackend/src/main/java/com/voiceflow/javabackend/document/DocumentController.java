package com.voiceflow.javabackend.document;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/documents")
@RequiredArgsConstructor
public class DocumentController {

    private final DocumentRepository documentRepository;

    @GetMapping
    public ResponseEntity<List<Document>> getDocuments(@RequestParam(required = false) UUID companyId) {
        List<Document> list = companyId != null
                ? documentRepository.findByCompanyId(companyId)
                : documentRepository.findAll();
        return ResponseEntity.ok(list);
    }
}
