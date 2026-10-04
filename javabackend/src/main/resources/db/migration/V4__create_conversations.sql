CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY,
    company_id UUID,
    customer_id UUID,
    channel VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    detected_intent VARCHAR(80),
    last_confidence DOUBLE PRECISION,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY,
    conversation_id UUID NOT NULL,
    sender VARCHAR(30) NOT NULL,
    content VARCHAR(4000) NOT NULL,
    intent VARCHAR(80),
    confidence DOUBLE PRECISION,
    escalated BOOLEAN NOT NULL DEFAULT FALSE,
    ticket_id VARCHAR(60),
    booking_id VARCHAR(60),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
