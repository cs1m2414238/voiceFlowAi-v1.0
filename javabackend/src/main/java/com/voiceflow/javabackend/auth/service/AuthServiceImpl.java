package com.voiceflow.javabackend.auth.service;

import com.voiceflow.javabackend.auth.dto.AuthRequest;
import com.voiceflow.javabackend.auth.dto.AuthResponse;
import com.voiceflow.javabackend.auth.dto.RegisterRequest;
import com.voiceflow.javabackend.common.security.JwtService;
import com.voiceflow.javabackend.company.entity.Company;
import com.voiceflow.javabackend.company.repository.CompanyRepository;
import com.voiceflow.javabackend.user.entity.User;
import com.voiceflow.javabackend.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.NoSuchElementException;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final UserRepository userRepository;
    private final CompanyRepository companyRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    @Override
    public AuthResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new IllegalArgumentException("User already exists with email: " + request.email());
        }

        Company company = companyRepository.findById(request.companyId())
                .orElseThrow(() -> new NoSuchElementException("Company not found with id: " + request.companyId()));

        String passwordHash = passwordEncoder.encode(request.password());

        User user = User.builder()
                .userName(request.userName())
                .email(request.email())
                .passwordHash(passwordHash)
                .role(request.role())
                .company(company)
                .build();

        User savedUser = userRepository.save(user);
        String token = jwtService.generateToken(savedUser);

        return new AuthResponse(
                token,
                savedUser.getUserId(),
                savedUser.getUserName(),
                savedUser.getEmail(),
                savedUser.getRole(),
                savedUser.getCompany().getId()
        );
    }

    @Override
    public AuthResponse login(AuthRequest request) {
        User user = userRepository.findByEmail(request.email())
                .orElseThrow(() -> new IllegalArgumentException("Invalid email or password"));

        if (!user.isActive()) {
            throw new IllegalStateException("User account is deactivated");
        }

        if (!passwordEncoder.matches(request.password(), user.getPasswordHash())) {
            throw new IllegalArgumentException("Invalid email or password");
        }

        String token = jwtService.generateToken(user);

        return new AuthResponse(
                token,
                user.getUserId(),
                user.getUserName(),
                user.getEmail(),
                user.getRole(),
                user.getCompany().getId()
        );
    }
}
