package com.voiceflow.javabackend.company.controller;

import com.voiceflow.javabackend.company.dto.CompanyCreateRequest;
import com.voiceflow.javabackend.company.dto.CompanyResponse;
import com.voiceflow.javabackend.company.dto.CompanyUpdateRequest;
import com.voiceflow.javabackend.company.entity.Company;
import com.voiceflow.javabackend.company.service.CompanyService;
import io.swagger.v3.oas.annotations.parameters.RequestBody;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;


@RestController
@RequestMapping("/api/companies")
@RequiredArgsConstructor
public class CompanyController {

    private CompanyService companyService;


    @PostMapping
    public ResponseEntity<CompanyResponse> createCompany(@Valid @RequestBody CompanyCreateRequest  request) {

        CompanyResponse response =companyService.createCompany(request);

        return ResponseEntity.status(HttpStatus.CREATED).body(response);

    }

    @GetMapping("/{id}")
    public ResponseEntity<CompanyResponse> getCompanyById(@PathVariable UUID id){

        CompanyResponse response = companyService.getCompanyById(id);

        return ResponseEntity.ok(response);

    }

    @GetMapping
    public ResponseEntity<List<CompanyResponse>> getAllCompany(){

        List<CompanyResponse> companies = companyService.getAllCompanies();

        return ResponseEntity.ok(companies);

    }

    @PatchMapping("/{id}")
    public ResponseEntity<CompanyResponse> updateCompany(@PathVariable UUID id,
                                                         @Valid @RequestBody CompanyUpdateRequest request) {

        CompanyResponse response = companyService.updateCompany(id, request);

        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCompany(@PathVariable UUID id){

        companyService.deleteCompany(id);
        return  ResponseEntity.noContent().build();
    }
}
