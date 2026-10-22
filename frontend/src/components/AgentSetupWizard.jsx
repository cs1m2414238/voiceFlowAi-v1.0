import React, { useState } from 'react';

export default function AgentSetupWizard() {
  const [step, setStep] = useState(1);
  const [selectedTemplate, setSelectedTemplate] = useState('ecommerce');
  const [isUploading, setIsUploading] = useState(false);

  const templates = [
    { id: 'ecommerce', name: 'E-Commerce', desc: 'Order tracking & product FAQs' },
    { id: 'healthcare', name: 'Healthcare', desc: 'Appointment scheduling & patient info' },
    { id: 'hotel', name: 'Hotels & Hospitality', desc: 'Room bookings & concierge' },
    { id: 'banking', name: 'Banking', desc: 'Account inquiries & fraud reporting' },
  ];

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-xl shadow-md border border-gray-100 my-10 font-sans text-gray-800">
      {/* Header */}
      <div className="mb-6">
        <span className="text-xs font-semibold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-full">
          UX Workflow Builder
        </span>
        <h1 className="text-2xl font-bold text-gray-900 mt-2">Configure Voice AI Agent</h1>
        <p className="text-sm text-gray-500">Step {step} of 3</p>
      </div>

      {/* Step Progress Bar */}
      <div className="w-full bg-gray-100 h-2 rounded-full mb-8 overflow-hidden">
        <div 
          className="bg-indigo-600 h-2 transition-all duration-300 ease-in-out"
          style={{ width: `${(step / 3) * 100}%` }}
        />
      </div>

      {/* Step 1: Select Template */}
      {step === 1 && (
        <div>
          <h2 className="text-lg font-semibold mb-1 text-gray-900">Select an Industry Template</h2>
          <p className="text-xs text-gray-500 mb-4">Choose a pre-configured workflow tailored to your business vertical.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            {templates.map((t) => (
              <div
                key={t.id}
                onClick={() => setSelectedTemplate(t.id)}
                className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  selectedTemplate === t.id 
                    ? 'border-indigo-600 bg-indigo-50/40 shadow-sm' 
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                }`}
              >
                <div className="flex justify-between items-center mb-1">
                  <h3 className="font-semibold text-gray-900">{t.name}</h3>
                  {selectedTemplate === t.id && (
                    <span className="h-2 w-2 rounded-full bg-indigo-600"></span>
                  )}
                </div>
                <p className="text-xs text-gray-500">{t.desc}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Step 2: Upload Knowledge Base */}
      {step === 2 && (
        <div>
          <h2 className="text-lg font-semibold mb-1 text-gray-900">Upload Knowledge Base (RAG)</h2>
          <p className="text-xs text-gray-500 mb-4">Provide documents for your AI agent to ground its responses in facts.</p>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center bg-gray-50 mb-6 hover:bg-gray-100/50 transition">
            <div className="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
              📁
            </div>
            <p className="text-sm font-medium text-gray-700 mb-1">Drag and drop business documents here</p>
            <p className="text-xs text-gray-400 mb-4">Supports PDF, DOCX, CSV up to 25MB</p>
            <button 
              onClick={() => setIsUploading(true)}
              className="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium hover:bg-gray-50 shadow-sm transition"
            >
              {isUploading ? "⚡ Indexing & Vectorizing..." : "Browse Files"}
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Voice & Persona Configuration */}
      {step === 3 && (
        <div>
          <h2 className="text-lg font-semibold mb-1 text-gray-900">Agent Persona & Voice</h2>
          <p className="text-xs text-gray-500 mb-4">Set prompt directives and natural speech parameters.</p>
          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">System Prompt Directives</label>
              <textarea 
                className="w-full border rounded-md p-3 text-sm text-gray-800 h-24 focus:ring-2 focus:ring-indigo-500 outline-none"
                defaultValue="You are a polite AI assistant for VoiceFlow. Answer questions using only the uploaded knowledge base."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Voice Profile (ElevenLabs TTS)</label>
              <select className="w-full border rounded-md p-2.5 text-sm text-gray-800 bg-white focus:ring-2 focus:ring-indigo-500 outline-none">
                <option>Rachel - Professional & Warm (Recommended)</option>
                <option>Adam - Natural & Conversational</option>
                <option>Sam - Expressive & Energetic</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Navigation Buttons */}
      <div className="flex justify-between mt-8 pt-4 border-t border-gray-100">
        <button
          onClick={() => setStep((s) => Math.max(1, s - 1))}
          disabled={step === 1}
          className="px-4 py-2 border rounded-md text-sm font-medium text-gray-600 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50"
        >
          Back
        </button>
        {step < 3 ? (
          <button
            onClick={() => setStep((s) => Math.min(3, s + 1))}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md text-sm font-medium hover:bg-indigo-700 transition"
          >
            Continue
          </button>
        ) : (
          <button
            onClick={() => alert("Voice Agent Successfully Deployed!")}
            className="px-4 py-2 bg-emerald-600 text-white rounded-md text-sm font-medium hover:bg-emerald-700 transition"
          >
            Deploy Voice Agent
          </button>
        )}
      </div>
    </div>
  );
}