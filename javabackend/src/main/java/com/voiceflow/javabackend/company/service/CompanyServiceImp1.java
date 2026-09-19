package com.voiceflow.javabackend.company.service;

import com.voiceflow.javabackend.company.dto.CompanyCreateRequest;
import com.voiceflow.javabackend.company.dto.CompanyResponse;
import com.voiceflow.javabackend.company.dto.CompanyUpdateRequest;
import com.voiceflow.javabackend.company.entity.Company;
import com.voiceflow.javabackend.company.mapper.CompanyMapper;
import com.voiceflow.javabackend.company.repository.CompanyRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.NoSuchElementException;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class CompanyServiceImp1 implements  CompanyService {

    private final CompanyRepository companyRepository;
    private final CompanyMapper companyMapper;

    @Override
    public CompanyResponse createCompany(CompanyCreateRequest request) {
        // dto to entity
        Company company = companyMapper.toEntity(request);

        // saved to repository
        Company savedCompany = companyRepository.save(company);

        // convert entity to dto
        return companyMapper.toResponse(savedCompany);

    }

    @Override
    public CompanyResponse getCompanyById(UUID id) {
        Company company = companyRepository
                .findById(id)
                .orElseThrow(() ->
                        new RuntimeException("Company not found with id: " + id)
                );
        return companyMapper.toResponse(company); // again returns entity converted in to dto

    }

    @Override
    public List<CompanyResponse> getAllCompanies() {
        return companyRepository
                .findAll()
                .stream()
                .map(companyMapper::toResponse)
                //.map(company -> companyMapper.toResponse(company)) equivalent to it
                .toList();
    }

    @Override
    public CompanyResponse updateCompany(UUID id, CompanyUpdateRequest request) {
        Company company = companyRepository
                .findById(id)
                .orElseThrow(() ->
                        new NoSuchElementException("Company not found with id: " + id)
                );

        companyMapper.updateEntity(company,request);

        Company updatedCompany = companyRepository.save(company);
        return companyMapper.toResponse(updatedCompany);
    }

    @Override
    public CompanyResponse deleteCompany(UUID id) {
        Company company = companyRepository
                .findById(id)
                .orElseThrow();

        companyRepository.delete(company);
        return null;
    }
}
