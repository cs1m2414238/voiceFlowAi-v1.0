package com.voiceflow.javabackend.user.service;

import com.voiceflow.javabackend.user.dto.UserCreateRequest;
import com.voiceflow.javabackend.user.dto.UserResponse;
import com.voiceflow.javabackend.user.dto.UserUpdateRequest;

import java.util.List;
import java.util.UUID;

public interface UserService {

    UserResponse createUser(UserCreateRequest request);

    UserResponse getUserById(UUID id);

    UserResponse getUserByEmail(String email);

    List<UserResponse> getAllUsers();

    UserResponse updateUser(
            UUID id,
            UserUpdateRequest request
    );

    void deleteUser(UUID id);
}
