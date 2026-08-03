package com.voiceflow.javabackend.company.entity;

import com.voiceflow.javabackend.company.enums.IndustryType;
import jakarta.persistence.*; // For jpa contains all annotations related to database
import lombok.*;  // for writing getter setter
import java.util.UUID;  // to generate a unique sr no for company
import java.time.LocalDateTime; // used for creation at a time

// for postgres
@Entity   // create a table for each company
@Table(name = "companies") /*  by default Hibernate creates company */
// lombok features
@Getter
@Setter
@NoArgsConstructor  // creates public Company(){} for spring & hibernate

@AllArgsConstructor
// creates
/*  public Company(
UUID id,
String name,
IndustryType industryType,
...
)*/
@Builder // builder can remove creation of object and using getter setter all that stuff
/*
* Company company=Company.builder()
.name("Amazon")
.industryType(IndustryType.ECOMMERCE)
.supportEmail("support@amazon.com")
.build();*/

public class Company {

    @Id //Every database table needs a primary key. it tells hibernate this field uniquely identifies a company.
    @GeneratedValue(strategy = GenerationType.UUID) // generates a0e1f54e... instead of company 1 company 2
    private UUID id;

    @Column(nullable = false,length = 150)
    private String name ;  // become in sql -> name VARCHAR(150) NOT NULL


    @Enumerated(EnumType.STRING)
    @Column(nullable = false) // means in a column of Industry type  which is not null ,it stores string form enum IndustryType
    private IndustryType industryType;  // stores HOTEL  ECOMMERCE instead of 0,1,2,3  cuz by Default its ORDINAL

    @Column(length = 150)
    private String supportEmail;

    @Column(length = 20)
    private String supportPhone;

    @Column(nullable = false)  // this means NOT NULL In sql
    private boolean active = true;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt; // time at creation/registration  of table for a company

    private LocalDateTime updatedAt; // time for update in any entry

    @PrePersist   // hibernates cycle callback
    public void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    public void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}