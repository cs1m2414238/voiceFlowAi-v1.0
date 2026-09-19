package com.voiceflow.javabackend.company.mapper;

import com.voiceflow.javabackend.company.dto.CompanyCreateRequest;
import com.voiceflow.javabackend.company.dto.CompanyResponse;
import com.voiceflow.javabackend.company.dto.CompanyUpdateRequest;
import com.voiceflow.javabackend.company.entity.Company;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class CompanyMapper {

    public Company toEntity(CompanyCreateRequest request){
        // CREATE DTO → ENTITY
        return Company.builder()
                .name(request.companyName())
                .industryType(request.industryType())
                .supportEmail(request.supportEmail())
                .supportPhone(request.supportPhone())
                .build();
    }

    public CompanyResponse toResponse(Company company){
        //Entity to Response DTO
        return new CompanyResponse(
                company.getId(),
                company.getName(),
                company.getIndustryType(),
                company.getCreatedAt(),
                company.getUpdatedAt(),
                company.getSupportEmail(),
                company.getSupportPhone(),
                company.isActive()
        );

    }
    public void updateEntity(Company company, CompanyUpdateRequest request ){
        if(request.companyName() != null) {
            company.setName(request.companyName());
        }
        if (request.industryType() != null) {
            company.setIndustryType(request.industryType());
        }

        if (request.supportEmail() != null) {
            company.setSupportEmail(request.supportEmail());
        }

        if (request.supportPhone() != null) {
            company.setSupportPhone(request.supportPhone());
        }

        if (request.active() != null) {
            company.setActive(request.active());
        }
    }

}
