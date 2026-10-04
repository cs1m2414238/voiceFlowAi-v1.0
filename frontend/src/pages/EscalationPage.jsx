import React, { useState, useEffect } from 'react';
import { getEscalations, resolveEscalation } from '../api/conversationApi';

export default function EscalationPage() {
  const [escalations, setEscalations] = useState([]);
  const [filter, setFilter] = useState('ALL');
  const [notesById, setNotesById] = useState({});

  const loadEscalations = async () => {
    const list = await getEscalations();
    setEscalations(list || []);
  };

  useEffect(() => {
    loadEscalations();
  }, []);

  const handleResolve = async (id) => {
    const notes = notesById[id] || 'Handled by human support agent and confirmed with customer.';
    await resolveEscalation(id, notes);
    await loadEscalations();
  };

  const filtered = escalations.filter((e) => (filter === 'ALL' ? true : e.status === filter));

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-rose-400 bg-rose-500/10 px-3 py-1 rounded-full border border-rose-500/20">
            Human-in-the-Loop Queue
          </span>
          <h2 className="text-2xl font-bold text-white mt-2">Escalations &amp; Complaint Tickets</h2>
          <p className="text-xs text-slate-400 mt-1">
            Automatically triggered when AI confidence &lt; 0.60, intent is <code className="text-rose-400">complaint</code> / <code className="text-rose-400">human</code>, or customer requests supervisor
          </p>
        </div>

        <div className="flex gap-2">
          {['ALL', 'OPEN', 'RESOLVED'].map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold border transition ${
                filter === status
                  ? 'bg-indigo-600 text-white border-indigo-500'
                  : 'bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700'
              }`}
            >
              {status}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        {filtered.length === 0 && (
          <div className="text-center py-12 text-xs text-slate-500">
            No escalations match filter &quot;{filter}&quot;.
          </div>
        )}

        {filtered.map((esc) => (
          <div
            key={esc.id}
            className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 flex flex-col lg:flex-row lg:items-center justify-between gap-4"
          >
            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <span
                  className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                    esc.status === 'OPEN'
                      ? 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
                      : 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                  }`}
                >
                  {esc.status}
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono bg-amber-500/10 text-amber-300 border border-amber-500/20">
                  🎫 {esc.ticketId || 'TKT-PENDING'}
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                  intent: {esc.intent} ({Math.round((esc.confidence ?? 0.5) * 100)}% conf)
                </span>
                <span className="text-xs font-bold text-white">{esc.customerName}</span>
              </div>

              <p className="text-xs text-slate-200">{esc.reason}</p>

              <div className="text-[11px] text-slate-500 flex flex-wrap gap-4">
                <span>Conversation: <code className="text-slate-400">{esc.conversationId}</code></span>
                <span>Priority: <strong className="text-rose-400">{esc.priority || 'HIGH'}</strong></span>
                <span>Created: {new Date(esc.createdAt).toLocaleString()}</span>
                {esc.resolvedAt && <span>Resolved: {new Date(esc.resolvedAt).toLocaleString()}</span>}
              </div>
            </div>

            {esc.status === 'OPEN' ? (
              <div className="flex flex-col sm:flex-row gap-2 min-w-[280px]">
                <input
                  type="text"
                  value={notesById[esc.id] || ''}
                  onChange={(e) => setNotesById({ ...notesById, [esc.id]: e.target.value })}
                  placeholder="Resolution notes..."
                  className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                />
                <button
                  onClick={() => handleResolve(esc.id)}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-emerald-600/20 transition whitespace-nowrap"
                >
                  ✓ Mark Resolved
                </button>
              </div>
            ) : (
              <div className="text-xs text-emerald-400 font-semibold">
                ✓ Handled by Support Team
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
