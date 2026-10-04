package com.voiceflow.javabackend.customer.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

public record CustomerCreateRequest(
        @NotNull(message = "Company ID is required")
        UUID companyId,

        @NotBlank(message = "Customer name is required")
        String name,

        @Email(message = "Email must be valid")
        String email,

        String phone
) {
}
