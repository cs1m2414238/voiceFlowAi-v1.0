package com.voiceflow.javabackend.company.dto;

import com.voiceflow.javabackend.company.enums.IndustryType;

import java.time.LocalDateTime;
import java.util.UUID;

public record CompanyResponse (
       UUID id,
       String name ,
       IndustryType industryType,
       LocalDateTime createdAt,
       LocalDateTime updatedAt,
       String supportPhone,
       String supportEmail,
       boolean active
){}