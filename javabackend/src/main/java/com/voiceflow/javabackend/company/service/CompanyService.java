    package com.voiceflow.javabackend.company.service;

    import com.voiceflow.javabackend.company.dto.CompanyCreateRequest;
    import com.voiceflow.javabackend.company.dto.CompanyResponse;
    import com.voiceflow.javabackend.company.dto.CompanyUpdateRequest;

    import java.util.List;
    import java.util.UUID;

    public interface CompanyService {
        CompanyResponse createCompany(CompanyCreateRequest request);
        CompanyResponse getCompanyById(UUID id);
        List<CompanyResponse> getAllCompanies();


        CompanyResponse updateCompany(
                UUID id,
                CompanyUpdateRequest request
        );

        CompanyResponse deleteCompany(UUID id);




}
