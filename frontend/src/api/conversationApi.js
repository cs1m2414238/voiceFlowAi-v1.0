import { getAuthHeaders } from './authApi';

const CONV_STORAGE_KEY = 'vf_conversations_store';
const ESC_STORAGE_KEY = 'vf_escalations_store';

const INITIAL_CONVERSATIONS = [
  {
    id: 'conv-1001',
    companyId: '11111111-1111-1111-1111-111111111111',
    customerName: 'Aarav Mehta',
    channel: 'VOICE',
    status: 'ACTIVE',
    detectedIntent: 'order',
    lastConfidence: 0.94,
    startedAt: new Date(Date.now() - 18 * 60000).toISOString(),
    messages: [
      {
        id: 'm-1',
        sender: 'customer',
        content: 'Where is my order #ORD-4821?',
        timestamp: new Date(Date.now() - 17 * 60000).toISOString(),
      },
      {
        id: 'm-2',
        sender: 'agent',
        content: 'Your order #ORD-4821 is currently in transit and scheduled for delivery tomorrow by 6 PM.',
        intent: 'order',
        confidence: 0.94,
        escalated: false,
        timestamp: new Date(Date.now() - 16 * 60000).toISOString(),
      },
    ],
  },
  {
    id: 'conv-1002',
    companyId: '11111111-1111-1111-1111-111111111111',
    customerName: 'Sarah Jenkins',
    channel: 'CHAT',
    status: 'ESCALATED',
    detectedIntent: 'complaint',
    lastConfidence: 0.88,
    ticketId: 'TKT-90341',
    startedAt: new Date(Date.now() - 45 * 60000).toISOString(),
    messages: [
      {
        id: 'm-3',
        sender: 'customer',
        content: 'My package arrived damaged and I want an immediate replacement or human supervisor.',
        timestamp: new Date(Date.now() - 44 * 60000).toISOString(),
      },
      {
        id: 'm-4',
        sender: 'agent',
        content: 'I apologize for the damaged package. I have logged complaint ticket TKT-90341 and escalated this conversation to a human specialist.',
        intent: 'complaint',
        confidence: 0.88,
        escalated: true,
        ticket_id: 'TKT-90341',
        timestamp: new Date(Date.now() - 43 * 60000).toISOString(),
      },
    ],
  },
  {
    id: 'conv-1003',
    companyId: '22222222-2222-2222-2222-222222222222',
    customerName: 'Rohan Kulkarni',
    channel: 'VOICE',
    status: 'COMPLETED',
    detectedIntent: 'booking',
    lastConfidence: 0.96,
    bookingId: 'BKG-77412',
    startedAt: new Date(Date.now() - 120 * 60000).toISOString(),
    endedAt: new Date(Date.now() - 115 * 60000).toISOString(),
    messages: [
      {
        id: 'm-5',
        sender: 'customer',
        content: 'Can I book a dental checkup for tomorrow at 10 AM?',
        timestamp: new Date(Date.now() - 119 * 60000).toISOString(),
      },
      {
        id: 'm-6',
        sender: 'agent',
        content: 'Your appointment is confirmed for tomorrow at 10:00 AM. Booking reference: BKG-77412.',
        intent: 'booking',
        confidence: 0.96,
        escalated: false,
        booking_id: 'BKG-77412',
        timestamp: new Date(Date.now() - 118 * 60000).toISOString(),
      },
    ],
  },
];

const INITIAL_ESCALATIONS = [
  {
    id: 'esc-501',
    conversationId: 'conv-1002',
    companyId: '11111111-1111-1111-1111-111111111111',
    customerName: 'Sarah Jenkins',
    reason: 'Damaged shipment complaint & request for human supervisor',
    intent: 'complaint',
    confidence: 0.88,
    ticketId: 'TKT-90341',
    priority: 'HIGH',
    status: 'OPEN',
    createdAt: new Date(Date.now() - 43 * 60000).toISOString(),
  },
  {
    id: 'esc-502',
    conversationId: 'conv-1004',
    companyId: '33333333-3333-3333-3333-333333333333',
    customerName: 'Vikram Singh',
    reason: 'Low confidence (0.42) on custom corporate banquet billing dispute',
    intent: 'human',
    confidence: 0.42,
    ticketId: 'TKT-90389',
    priority: 'CRITICAL',
    status: 'OPEN',
    createdAt: new Date(Date.now() - 25 * 60000).toISOString(),
  },
  {
    id: 'esc-503',
    conversationId: 'conv-0998',
    companyId: '11111111-1111-1111-1111-111111111111',
    customerName: 'Elena Rostova',
    reason: 'Refund escalation for international customs charge',
    intent: 'complaint',
    confidence: 0.79,
    ticketId: 'TKT-90210',
    priority: 'MEDIUM',
    status: 'RESOLVED',
    createdAt: new Date(Date.now() - 240 * 60000).toISOString(),
    resolvedAt: new Date(Date.now() - 180 * 60000).toISOString(),
  },
];

function readLocalConversations() {
  try {
    const raw = localStorage.getItem(CONV_STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    // ignore
  }
  localStorage.setItem(CONV_STORAGE_KEY, JSON.stringify(INITIAL_CONVERSATIONS));
  return INITIAL_CONVERSATIONS;
}

function writeLocalConversations(list) {
  try {
    localStorage.setItem(CONV_STORAGE_KEY, JSON.stringify(list));
  } catch {
    // ignore
  }
}

function readLocalEscalations() {
  try {
    const raw = localStorage.getItem(ESC_STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    // ignore
  }
  localStorage.setItem(ESC_STORAGE_KEY, JSON.stringify(INITIAL_ESCALATIONS));
  return INITIAL_ESCALATIONS;
}

function writeLocalEscalations(list) {
  try {
    localStorage.setItem(ESC_STORAGE_KEY, JSON.stringify(list));
  } catch {
    // ignore
  }
}

export async function createConversation(data) {
  try {
    const response = await fetch('/api/conversations', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Backend conversation endpoint unavailable');
    return await response.json();
  } catch {
    const conv = {
      id: `conv-${Date.now()}`,
      companyId: data.companyId || '11111111-1111-1111-1111-111111111111',
      customerName: data.customerName || 'Live Caller',
      channel: data.channel || 'VOICE',
      status: 'ACTIVE',
      detectedIntent: 'faq',
      lastConfidence: 1.0,
      startedAt: new Date().toISOString(),
      messages: [],
    };
    const all = [conv, ...readLocalConversations()];
    writeLocalConversations(all);
    return conv;
  }
}

export async function getConversations(companyId) {
  try {
    const query = companyId ? `?companyId=${encodeURIComponent(companyId)}` : '';
    const response = await fetch(`/api/conversations${query}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Backend conversation endpoint unavailable');
    return await response.json();
  } catch {
    const list = readLocalConversations();
    return companyId ? list.filter((c) => !c.companyId || c.companyId === companyId) : list;
  }
}

export async function getConversationById(id) {
  try {
    const response = await fetch(`/api/conversations/${id}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Backend conversation endpoint unavailable');
    return await response.json();
  } catch {
    return readLocalConversations().find((c) => c.id === id) || null;
  }
}

export async function sendMessage(conversationId, content, sender = 'customer', metadata = {}) {
  try {
    const response = await fetch(`/api/conversations/${conversationId}/messages`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ content, sender, ...metadata }),
    });
    if (!response.ok) throw new Error('Backend message endpoint unavailable');
    return await response.json();
  } catch {
    const msg = {
      id: `msg-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      conversationId,
      sender,
      content,
      timestamp: new Date().toISOString(),
      ...metadata,
    };
    const list = readLocalConversations().map((c) => {
      if (c.id !== conversationId) return c;
      const updatedMessages = [...(c.messages || []), msg];
      return {
        ...c,
        detectedIntent: metadata.intent || c.detectedIntent,
        lastConfidence: metadata.confidence ?? c.lastConfidence,
        status: metadata.escalated ? 'ESCALATED' : c.status,
        ticketId: metadata.ticket_id || c.ticketId,
        bookingId: metadata.booking_id || c.bookingId,
        messages: updatedMessages,
      };
    });
    writeLocalConversations(list);

    if (metadata.escalated) {
      const targetConv = list.find((c) => c.id === conversationId);
      const escalations = readLocalEscalations();
      const exists = escalations.some((e) => e.conversationId === conversationId && e.status === 'OPEN');
      if (!exists) {
        escalations.unshift({
          id: `esc-${Date.now()}`,
          conversationId,
          companyId: targetConv?.companyId || '11111111-1111-1111-1111-111111111111',
          customerName: targetConv?.customerName || 'Customer',
          reason: content,
          intent: metadata.intent || 'human',
          confidence: metadata.confidence ?? 0.5,
          ticketId: metadata.ticket_id || `TKT-${Math.floor(10000 + Math.random() * 90000)}`,
          priority: 'HIGH',
          status: 'OPEN',
          createdAt: new Date().toISOString(),
        });
        writeLocalEscalations(escalations);
      }
    }

    return msg;
  }
}

export async function getMessages(conversationId) {
  try {
    const response = await fetch(`/api/conversations/${conversationId}/messages`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Backend messages endpoint unavailable');
    return await response.json();
  } catch {
    const conv = readLocalConversations().find((c) => c.id === conversationId);
    return conv?.messages || [];
  }
}

export async function endConversation(id) {
  try {
    const response = await fetch(`/api/conversations/${id}/end`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Backend end conversation endpoint unavailable');
    return await response.json();
  } catch {
    const list = readLocalConversations().map((c) =>
      c.id === id ? { ...c, status: 'COMPLETED', endedAt: new Date().toISOString() } : c
    );
    writeLocalConversations(list);
    return list.find((c) => c.id === id);
  }
}

export async function getEscalations(companyId) {
  try {
    const query = companyId ? `?companyId=${encodeURIComponent(companyId)}` : '';
    const response = await fetch(`/api/escalations${query}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Backend escalations endpoint unavailable');
    return await response.json();
  } catch {
    const list = readLocalEscalations();
    return companyId ? list.filter((e) => !e.companyId || e.companyId === companyId) : list;
  }
}

export async function resolveEscalation(id, resolutionNotes = 'Resolved by support agent') {
  try {
    const response = await fetch(`/api/escalations/${id}/resolve`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ resolutionNotes }),
    });
    if (!response.ok) throw new Error('Backend escalation resolve endpoint unavailable');
    return await response.json();
  } catch {
    const list = readLocalEscalations().map((e) =>
      e.id === id
        ? {
            ...e,
            status: 'RESOLVED',
            resolutionNotes,
            resolvedAt: new Date().toISOString(),
          }
        : e
    );
    writeLocalEscalations(list);
    return list.find((e) => e.id === id);
  }
}
