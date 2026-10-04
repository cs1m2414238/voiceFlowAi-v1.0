package com.voiceflow.javabackend.user.mapper;

import com.voiceflow.javabackend.company.entity.Company;
import com.voiceflow.javabackend.user.dto.UserCreateRequest;
import com.voiceflow.javabackend.user.dto.UserResponse;
import com.voiceflow.javabackend.user.dto.UserUpdateRequest;
import com.voiceflow.javabackend.user.entity.User;
import org.springframework.stereotype.Component;

@Component
public class UserMapper {

    public User toEntity(
            UserCreateRequest request,
            Company company,
            String passwordHash
    ) {
        return User.builder()
                .userName(request.userName())
                .email(request.email())
                .passwordHash(passwordHash)
                .role(request.role())
                .company(company)
                .build();
    }

    public UserResponse toResponse(User user) {
        return new UserResponse(
                user.getUserId(),
                user.getUserName(),
                user.getEmail(),
                user.isActive(),
                user.getRole(),
                user.getCompany().getId(),
                user.getCompany().getName(),
                user.getCreatedAt(),
                user.getUpdatedAt()
        );
    }

    public void updateEntity(
            User user,
            UserUpdateRequest request
    ) {
        if (request.userName() != null) {
            user.setUserName(request.userName());
        }
        if (request.email() != null) {
            user.setEmail(request.email());
        }
        if (request.role() != null) {
            user.setRole(request.role());
        }
        if (request.active() != null) {
            user.setActive(request.active());
        }
    }
}
