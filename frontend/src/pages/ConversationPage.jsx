import React, { useState, useEffect } from 'react';
import {
  getConversations,
  createConversation,
  sendMessage,
  endConversation,
} from '../api/conversationApi';
import { chatWithAgent, synthesizeSpeech } from '../api/voiceApi';

export default function ConversationPage() {
  const [conversations, setConversations] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [input, setInput] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [sending, setSending] = useState(false);
  const [autoTts, setAutoTts] = useState(false);

  const loadList = async () => {
    const list = await getConversations();
    setConversations(list || []);
    if (!selectedId && list && list.length > 0) {
      setSelectedId(list[0].id);
    }
  };

  useEffect(() => {
    loadList();
  }, []);

  const activeConv = conversations.find((c) => c.id === selectedId) || conversations[0] || null;

  const handleNewConversation = async (e) => {
    e.preventDefault();
    const created = await createConversation({
      customerName: customerName.trim() || `Caller #${Math.floor(100 + Math.random() * 900)}`,
      channel: 'VOICE',
    });
    setCustomerName('');
    await loadList();
    setSelectedId(created.id);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || !activeConv) return;

    const question = input.trim();
    setInput('');
    setSending(true);

    try {
      await sendMessage(activeConv.id, question, 'customer');

      // Invoke Python AI Service LangGraph orchestrator
      const aiRes = await chatWithAgent({
        question,
        companyId: activeConv.companyId || 'default',
        sessionId: activeConv.id,
      });

      await sendMessage(activeConv.id, aiRes.answer, 'agent', {
        intent: aiRes.intent,
        confidence: aiRes.confidence,
        escalated: aiRes.escalated,
        ticket_id: aiRes.ticket_id,
        booking_id: aiRes.booking_id,
      });

      if (autoTts && aiRes.answer) {
        synthesizeSpeech(aiRes.answer, 'Rachel');
      }

      await loadList();
    } finally {
      setSending(false);
    }
  };

  const handleEndSession = async () => {
    if (!activeConv) return;
    await endConversation(activeConv.id);
    await loadList();
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left Sidebar: Sessions List & New Session */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4 h-fit">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white">Conversation Sessions</h3>
          <span className="text-xs font-mono text-indigo-400">{conversations.length} total</span>
        </div>

        <form onSubmit={handleNewConversation} className="flex gap-2">
          <input
            type="text"
            value={customerName}
            onChange={(e) => setCustomerName(e.target.value)}
            placeholder="New caller name..."
            className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
          />
          <button
            type="submit"
            className="px-3.5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-bold transition"
          >
            + Start
          </button>
        </form>

        <div className="space-y-2 max-h-[420px] overflow-y-auto pr-1">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => setSelectedId(conv.id)}
              className={`p-3.5 rounded-xl border cursor-pointer transition text-xs ${
                activeConv?.id === conv.id
                  ? 'bg-indigo-600/15 border-indigo-500'
                  : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex justify-between items-center">
                <span className="font-bold text-white">{conv.customerName || conv.id}</span>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                    conv.status === 'ESCALATED'
                      ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      : conv.status === 'ACTIVE'
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                      : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {conv.status}
                </span>
              </div>
              <div className="flex items-center gap-2 mt-1.5 text-[11px] text-slate-400">
                <span>Intent: <code className="text-indigo-300">{conv.detectedIntent || 'faq'}</code></span>
                <span>•</span>
                <span>Conf: {Math.round((conv.lastConfidence ?? 0.9) * 100)}%</span>
              </div>
              {(conv.ticketId || conv.bookingId) && (
                <div className="flex gap-2 mt-1.5">
                  {conv.ticketId && (
                    <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20 text-[10px] font-mono">
                      🎫 {conv.ticketId}
                    </span>
                  )}
                  {conv.bookingId && (
                    <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 text-[10px] font-mono">
                      📅 {conv.bookingId}
                    </span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Right Panel: Multi-turn Transcript & Agent Metadata */}
      <div className="lg:col-span-2 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
        {activeConv ? (
          <>
            <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-lg font-bold text-white">{activeConv.customerName || activeConv.id}</h3>
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    {activeConv.channel}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  Session ID: <code className="text-slate-300">{activeConv.id}</code> • LangGraph Multi-Agent Orchestrator
                </p>
              </div>

              <div className="flex items-center gap-2">
                <label className="flex items-center gap-1.5 text-xs text-slate-300 cursor-pointer bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
                  <input
                    type="checkbox"
                    checked={autoTts}
                    onChange={(e) => setAutoTts(e.target.checked)}
                    className="accent-indigo-500"
                  />
                  🔊 Speak Replies
                </label>
                {activeConv.status !== 'COMPLETED' && (
                  <button
                    onClick={handleEndSession}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold transition"
                  >
                    End Call
                  </button>
                )}
              </div>
            </div>

            {/* Messages Feed */}
            <div className="my-4 h-80 overflow-y-auto space-y-3 p-4 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs">
              {(activeConv.messages || []).length === 0 && (
                <p className="text-slate-500 text-center py-12">
                  No messages yet. Ask about orders, bookings, FAQs, recommendations, or complaints below.
                </p>
              )}
              {(activeConv.messages || []).map((m) => (
                <div
                  key={m.id}
                  className={`flex ${m.sender === 'customer' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[82%] p-3.5 rounded-2xl space-y-1.5 ${
                      m.sender === 'customer'
                        ? 'bg-indigo-600 text-white rounded-br-none'
                        : 'bg-slate-800/90 text-slate-100 rounded-bl-none border border-slate-700'
                    }`}
                  >
                    <p className="leading-relaxed">{m.content}</p>
                    {m.sender === 'agent' && (
                      <div className="flex flex-wrap items-center gap-1.5 pt-1.5 border-t border-slate-700/80 text-[10px]">
                        {m.intent && (
                          <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono">
                            intent: {m.intent}
                          </span>
                        )}
                        {m.confidence !== undefined && (
                          <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">
                            conf: {Math.round(m.confidence * 100)}%
                          </span>
                        )}
                        {m.ticket_id && (
                          <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono">
                            ticket: {m.ticket_id}
                          </span>
                        )}
                        {m.booking_id && (
                          <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-mono">
                            booking: {m.booking_id}
                          </span>
                        )}
                        {m.escalated && (
                          <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">
                            ⚠️ ESCALATED TO HUMAN
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Quick Prompt Chips & Input */}
            <div className="space-y-2">
              <div className="flex flex-wrap gap-1.5">
                {[
                  'Where is my order #ORD-4821?',
                  'Book an appointment for tomorrow at 3 PM',
                  'My item arrived damaged, I want a refund',
                  'Recommend the best plan for our clinic',
                ].map((sample, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => setInput(sample)}
                    className="text-[11px] px-2.5 py-1 rounded-full bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-800 transition"
                  >
                    {sample}
                  </button>
                ))}
              </div>

              <form onSubmit={handleSend} className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type customer utterance to route through LangGraph..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
                />
                <button
                  type="submit"
                  disabled={sending}
                  className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-xl text-xs font-bold shadow-lg shadow-indigo-600/20 transition"
                >
                  {sending ? 'Routing...' : 'Send'}
                </button>
              </form>
            </div>
          </>
        ) : (
          <div className="text-center py-12 text-slate-400 text-xs">
            Select or create a conversation to begin testing.
          </div>
        )}
      </div>
    </div>
  );
}
