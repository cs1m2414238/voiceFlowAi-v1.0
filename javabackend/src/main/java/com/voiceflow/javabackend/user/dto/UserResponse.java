package com.voiceflow.javabackend.user.dto;

import com.voiceflow.javabackend.user.enums.UserRole;

import java.time.LocalDateTime;
import java.util.UUID;

public record  UserResponse(
        UUID userId,
        String userName,
        String email,
        boolean active,
        UserRole role,

        UUID companyID,
        String companyName,

        LocalDateTime createdAt,
        LocalDateTime updatedAt
) {
}
