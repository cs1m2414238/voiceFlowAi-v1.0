# AI Service API contract

## POST /agent/chat

Request (JSON):
| field | type | notes |
|---|---|---|
| question | string | the customer's message (required) |
| company_id | string | which company's knowledge base to use |
| session_id | string | one per call or conversation |

Response (JSON):
| field | type | notes |
|---|---|---|
| answer | string | text to speak or show |
| intent | string | faq, booking, order, complaint, recommendation, human |
| confidence | number | 0 to 1 |
| escalated | boolean | true means hand over to a human |
| ticket_id | string or null | set when a complaint ticket is created |

Field names use snake_case. Java DTOs should map them with @JsonProperty.