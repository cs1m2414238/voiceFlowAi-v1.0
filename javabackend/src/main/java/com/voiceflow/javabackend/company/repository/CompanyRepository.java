package com.voiceflow.javabackend.company.repository;

import com.voiceflow.javabackend.company.entity.Company;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface CompanyRepository extends JpaRepository<Company, UUID> {
}
