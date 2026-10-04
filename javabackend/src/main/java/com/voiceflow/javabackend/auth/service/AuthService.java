package com.voiceflow.javabackend.auth.service;

import com.voiceflow.javabackend.auth.dto.AuthRequest;
import com.voiceflow.javabackend.auth.dto.AuthResponse;
import com.voiceflow.javabackend.auth.dto.RegisterRequest;

public interface AuthService {

    AuthResponse register(RegisterRequest request);

    AuthResponse login(AuthRequest request);
}
