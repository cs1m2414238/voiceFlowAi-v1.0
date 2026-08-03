# Company Module

## Purpose

The Company module is the root module of the VoiceFlow AI platform.

VoiceFlow AI is a multi-tenant SaaS application where multiple companies
register and use the platform independently.

Examples:

- Amazon
- Apollo Hospital
- Taj Hotel
- Swiggy
- Domino's

Every company has its own:

- Users
- Customers
- Conversations
- Documents
- Agent Configuration
- Bookings
- Orders
- Complaints

---

# Package Structure

company/
├── entity/
├── enums/
├── repository/
├── service/
├── controller/
├── dto/
└── mapper/

---

# Entity

## Company.java

Represents one company in the platform.

Fields

- id
- name
- industryType
- supportEmail
- supportPhone
- active
- createdAt
- updatedAt

Annotations

@Entity
Represents a database table.

@Table
Specifies the database table name.

@Id
Primary key.

@GeneratedValue
Automatically generates UUID.

@Column
Defines column properties.

@Enumerated(EnumType.STRING)
Stores enum values as text.

@PrePersist
Automatically sets createdAt and updatedAt before insert.

@PreUpdate
Automatically updates updatedAt before update.

---

# Enum

## IndustryType

Defines business category.

Example values

- HOTEL
- ECOMMERCE
- HEALTHCARE
- EDUCATION
- BANKING
- RESTAURANT
- OTHER

---

# Repository

## CompanyRepository

Responsible only for database operations.

Example

- save()
- findById()
- findAll()
- delete()

Repository should NOT contain business logic.

---

# Service

## CompanyService

Contains business rules.

Examples

- Create Company
- Update Company
- Deactivate Company
- Validate Company

Service communicates with Repository.

Flow

Controller
↓

Service
↓

Repository
↓

Database

---

# Controller

## CompanyController

Receives HTTP requests.

Example APIs

POST /api/companies

GET /api/companies/{id}

PUT /api/companies/{id}

DELETE /api/companies/{id}

Controller should NOT contain business logic.

It should only:

- Receive request
- Validate request
- Call service
- Return response

---

# DTO

DTO stands for Data Transfer Object.

Request DTO

CompanyCreateRequest

Response DTO

CompanyResponse

Never expose Entity directly to the frontend.

Correct flow

Frontend

↓

Request DTO

↓

Controller

↓

Service

↓

Repository

↓

Database

↓

Repository

↓

Service

↓

Response DTO

↓

Frontend

---

# Mapper

Mapper converts

DTO ⇄ Entity

Example

CompanyCreateRequest

↓

Company

and

Company

↓

CompanyResponse

---

# Database Table

companies

Columns

- id
- name
- industry_type
- support_email
- support_phone
- active
- created_at
- updated_at

---

# Complete Request Flow

Client

↓

POST /api/companies

↓

CompanyController

↓

CompanyService

↓

CompanyRepository

↓

PostgreSQL

↓

CompanyRepository

↓

CompanyService

↓

CompanyResponse

↓

Client

---

# Current Goal

Finish the Company module before starting

- Authentication
- Customer
- Conversation
- AI Integration

The Company module is the foundation of the entire application.