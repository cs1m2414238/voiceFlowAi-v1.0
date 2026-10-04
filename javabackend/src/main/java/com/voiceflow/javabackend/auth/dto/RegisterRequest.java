package com.voiceflow.javabackend.auth.dto;

import com.voiceflow.javabackend.user.enums.UserRole;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.util.UUID;

public record RegisterRequest(

        @NotBlank(message = "Username is required")
        @Size(max = 100)
        String userName,

        @NotBlank(message = "Email is required")
        @Email(message = "Email must be valid")
        @Size(max = 150)
        String email,

        @NotBlank(message = "Password is required")
        @Size(min = 8, max = 100)
        String password,

        @NotNull(message = "Role is required")
        UserRole role,

        @NotNull(message = "Company id is required")
        UUID companyId

) {
}