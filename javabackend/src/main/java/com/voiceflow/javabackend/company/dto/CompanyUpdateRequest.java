package com.voiceflow.javabackend.company.dto;

import com.voiceflow.javabackend.company.enums.IndustryType;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Size;

public record CompanyUpdateRequest(

        @Size(max = 150)
        String companyName,

        IndustryType industryType,

        @Email(message = "Support email must be valid")
        @Size(max = 150)
        String supportEmail,

        @Size(max = 20)
        String supportPhone,

        Boolean active
) {
}
