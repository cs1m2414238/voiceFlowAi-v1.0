package com.voiceflow.javabackend.company.dto;

import com.voiceflow.javabackend.company.enums.IndustryType;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record CompanyCreateRequest (
        @Email(message = "Support email must be valid")
        @Size(max =150)
        String supportEmail,

        @NotBlank(message = "Company name is required")
        @Size(max= 150)
        String companyName,

        @NotNull(message = "Industry type can't be null")
        IndustryType industryType,

        @Size(max = 20)
        @NotNull(message = "support phone can't be null")
        String supportPhone
){}
