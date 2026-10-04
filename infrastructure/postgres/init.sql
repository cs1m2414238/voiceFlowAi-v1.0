-- VoiceFlow AI Platform PostgreSQL Initialization Script
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Companies Table
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    industry_type VARCHAR(50) NOT NULL,
    support_email VARCHAR(150),
    support_phone VARCHAR(20),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Customers Table
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. Conversations Table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
    channel VARCHAR(30) NOT NULL DEFAULT 'VOICE',
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    detected_intent VARCHAR(50),
    last_confidence DOUBLE PRECISION,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP
);

-- 5. Seed Default Demo Companies
INSERT INTO companies (id, name, industry_type, support_email, support_phone, active)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'NovaMart E-Commerce', 'ECOMMERCE', 'support@novamart.io', '+1-800-555-0191', TRUE),
    ('22222222-2222-2222-2222-222222222222', 'Apex Care Medical Clinic', 'HEALTHCARE', 'care@apexmedical.org', '+1-800-555-0144', TRUE),
    ('33333333-3333-3333-3333-333333333333', 'Grand Horizon Hotels', 'HOTEL', 'concierge@grandhorizon.com', '+1-800-555-0178', TRUE)
ON CONFLICT (id) DO NOTHING;
