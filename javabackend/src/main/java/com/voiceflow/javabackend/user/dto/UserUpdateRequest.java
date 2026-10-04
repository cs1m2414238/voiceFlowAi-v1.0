package com.voiceflow.javabackend.user.dto;

import com.voiceflow.javabackend.user.enums.UserRole;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Size;

import java.util.UUID;

public record UserUpdateRequest(
        @Size(max = 100)
        String userName,

        @Email(message = "Email must be valid")
        @Size(max = 150)
        String email,

        UserRole role,

        Boolean active,

        UUID companyId
) {
}