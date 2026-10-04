package com.voiceflow.javabackend.auth.dto;

import com.voiceflow.javabackend.user.enums.UserRole;

import java.util.UUID;

public record AuthResponse(

        String token,
        UUID userId,
        String userName,
        String email,
        UserRole role,
        UUID companyId

) {
}