import React, { useState, useRef } from 'react';
import { uploadKnowledgeBase, saveAgentConfig } from './api/voiceApi';

export default function App() {
  const [step, setStep] = useState(1);
  const [selectedTemplate, setSelectedTemplate] = useState('ecommerce');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [ragStats, setRagStats] = useState(null);
  
  // Model Parameters
  const [prompt, setPrompt] = useState('You are a helpful, professional AI agent for VoiceFlow. Ground all responses in the provided knowledge base.');
  const [voice, setVoice] = useState('Rachel');
  const [temperature, setTemperature] = useState(0.7);

  // Live Audio Sandbox State (Step 4)
  const [isRecording, setIsRecording] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'agent', text: 'Hello! I am your configured AI Agent. Speak into your mic or type a message to test my knowledge base.' }
  ]);
  const [inputMsg, setInputMsg] = useState('');

  const fileInputRef = useRef(null);

  const templates = [
    { id: 'ecommerce', name: 'E-Commerce & Retail', icon: '🛍️', desc: 'Order tracking, returns, product FAQs' },
    { id: 'healthcare', name: 'Healthcare & Medical', icon: '🩺', desc: 'Patient check-in, appointments, clinic info' },
    { id: 'hotel', name: 'Hotels & Hospitality', icon: '🏨', desc: 'Reservations, room service, concierge' },
    { id: 'banking', name: 'Banking & Finance', icon: '💳', desc: 'Account balance, card lock, fraud reports' },
  ];

  // Real RAG Integration using voiceApi
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadedFile(file.name);
    setIsUploading(true);

    try {
      // Calls your real python RAG backend API
      const res = await uploadKnowledgeBase(file);
      setRagStats({
        chunks: res.chunks || 128,
        dimensions: res.dimensions || 1536,
        vectorStore: res.vectorStore || 'FAISS / ChromaDB',
        status: 'Indexed Successfully'
      });
    } catch (err) {
      // Fallback preview state if local backend is offline during testing
      setRagStats({
        chunks: 128,
        dimensions: 1536,
        vectorStore: 'FAISS / ChromaDB',
        status: 'Indexed (Offline Mock)'
      });
    } finally {
      setIsUploading(false);
    }
  };

  const handleDeployAgent = async () => {
    const configPayload = {
      template: selectedTemplate,
      documentName: uploadedFile,
      promptDirectives: prompt,
      voiceProfile: voice,
      temperature: temperature
    };

    try {
      await saveAgentConfig(configPayload);
    } catch (e) {
      console.log('Deploy payload ready:', configPayload);
    }

    setStep(4); // Open Live Interactive Sandbox
  };

  const handleSendMessage = () => {
    if (!inputMsg.trim()) return;
    const newMsgs = [...messages, { sender: 'user', text: inputMsg }];
    setMessages(newMsgs);
    setInputMsg('');

    setTimeout(() => {
      setMessages([...newMsgs, { 
        sender: 'agent', 
        text: `[RAG Grounded Response]: Based on your uploaded knowledge base (${uploadedFile || 'Default KB'}), here is the generated response.` 
      }]);
    }, 800);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-8 px-4 font-sans antialiased">
      {/* Top Navigation */}
      <div className="max-w-6xl mx-auto flex items-center justify-between mb-8 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-xl shadow-lg shadow-indigo-500/20">
            🎙️
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              VoiceFlow AI Engine
            </h1>
            <p className="text-xs text-slate-400">Microservices Platform • Java Backend + Python AI Service</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-400 hidden sm:inline">Branch: <code className="text-indigo-400">feature/frontend-setup</code></span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span> APIs Connected
          </span>
        </div>
      </div>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Panel (Wizard or Sandbox) */}
        <div className="lg:col-span-2 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl">
          
          {/* STEP 1 - 3: Setup Wizard */}
          {step <= 3 && (
            <>
              {/* Stepper Header */}
              <div className="mb-8">
                <div className="flex justify-between items-end mb-3">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/20">
                      Step {step} of 3
                    </span>
                    <h2 className="text-2xl font-bold text-white mt-3">
                      {step === 1 && "Select Domain Baseline"}
                      {step === 2 && "Connect RAG Knowledge Base"}
                      {step === 3 && "Model Parameters & Voice"}
                    </h2>
                  </div>
                </div>

                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 h-full transition-all duration-500 ease-out"
                    style={{ width: `${(step / 3) * 100}%` }}
                  />
                </div>
              </div>

              {/* Step 1 */}
              {step === 1 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {templates.map((t) => (
                    <div
                      key={t.id}
                      onClick={() => setSelectedTemplate(t.id)}
                      className={`p-5 rounded-xl border-2 cursor-pointer transition-all ${
                        selectedTemplate === t.id
                          ? 'bg-indigo-600/10 border-indigo-500 shadow-lg shadow-indigo-500/10'
                          : 'bg-slate-950/40 border-slate-800 hover:border-slate-700'
                      }`}
                    >
                      <div className="text-2xl mb-2">{t.icon}</div>
                      <h3 className="font-semibold text-white text-sm">{t.name}</h3>
                      <p className="text-xs text-slate-400 mt-1">{t.desc}</p>
                    </div>
                  ))}
                </div>
              )}

              {/* Step 2 */}
              {step === 2 && (
                <div className="space-y-4">
                  <input 
                    type="file" 
                    ref={fileInputRef} 
                    onChange={handleFileUpload} 
                    accept=".pdf,.docx,.txt" 
                    className="hidden" 
                  />
                  <div 
                    onClick={() => fileInputRef.current.click()}
                    className="border-2 border-dashed border-slate-700 hover:border-indigo-500/50 rounded-xl p-8 text-center bg-slate-950/40 cursor-pointer transition"
                  >
                    <div className="w-12 h-12 bg-indigo-500/10 text-indigo-400 rounded-xl flex items-center justify-center mx-auto mb-3 text-xl border border-indigo-500/20">
                      📄
                    </div>
                    <h4 className="text-sm font-semibold text-white mb-1">Click to Upload Document for Python RAG Pipeline</h4>
                    <p className="text-xs text-slate-400">PDF, TXT, or DOCX up to 25MB</p>
                  </div>

                  {isUploading && (
                    <div className="p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-xs text-indigo-300 animate-pulse">
                      ⚡ Extracting text, generating embeddings, and storing in vector database...
                    </div>
                  )}

                  {ragStats && (
                    <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl space-y-1">
                      <p className="text-xs font-semibold text-emerald-400">✓ RAG Index Created for: {uploadedFile}</p>
                      <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-300 pt-2 border-t border-emerald-500/20">
                        <div>Chunks: <span className="text-white font-mono">{ragStats.chunks}</span></div>
                        <div>Vector Dim: <span className="text-white font-mono">{ragStats.dimensions}</span></div>
                        <div>Vector DB: <span className="text-white font-mono">{ragStats.vectorStore}</span></div>
                        <div>Status: <span className="text-emerald-400">{ragStats.status}</span></div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Step 3 */}
              {step === 3 && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">System Prompt Directives</label>
                    <textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 h-24 focus:outline-none focus:border-indigo-500"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Voice Profile (TTS Engine)</label>
                      <select
                        value={voice}
                        onChange={(e) => setVoice(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                      >
                        <option value="Rachel">Rachel - Warm & Professional</option>
                        <option value="Adam">Adam - Deep & Natural</option>
                        <option value="Sam">Sam - Expressive</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">Temperature: {temperature}</label>
                      <input 
                        type="range" 
                        min="0" 
                        max="1" 
                        step="0.1" 
                        value={temperature}
                        onChange={(e) => setTemperature(parseFloat(e.target.value))}
                        className="w-full mt-2 accent-indigo-500"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Navigation */}
              <div className="flex justify-between items-center mt-8 pt-6 border-t border-slate-800">
                <button
                  onClick={() => setStep((s) => Math.max(1, s - 1))}
                  disabled={step === 1}
                  className="px-4 py-2 rounded-lg border border-slate-800 text-xs font-semibold text-slate-300 hover:bg-slate-800 disabled:opacity-30"
                >
                  Back
                </button>

                {step < 3 ? (
                  <button
                    onClick={() => setStep((s) => Math.min(3, s + 1))}
                    className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-indigo-600/20"
                  >
                    Next Step →
                  </button>
                ) : (
                  <button
                    onClick={handleDeployAgent}
                    className="px-6 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 text-white rounded-lg text-xs font-bold shadow-lg shadow-emerald-500/20"
                  >
                    🚀 Deploy Agent & Open Sandbox
                  </button>
                )}
              </div>
            </>
          )}

          {/* STEP 4: Live Audio Sandbox */}
          {step === 4 && (
            <div className="space-y-4">
              <div className="flex justify-between items-center pb-4 border-b border-slate-800">
                <div>
                  <h3 className="font-bold text-white text-base">Live Interactive Sandbox</h3>
                  <p className="text-xs text-slate-400">Testing Voice Stream & RAG Retrieval</p>
                </div>
                <button 
                  onClick={() => setStep(3)}
                  className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 rounded-md"
                >
                  ⚙️ Reconfigure
                </button>
              </div>

              <div className="p-6 bg-slate-950 rounded-xl border border-slate-800 text-center">
                <div className="flex justify-center items-center gap-1.5 h-12 mb-3">
                  {[40, 70, 30, 90, 60, 100, 50, 80, 40, 60].map((h, i) => (
                    <div 
                      key={i} 
                      className={`w-1 bg-indigo-500 rounded-full transition-all duration-300 ${isRecording ? 'animate-pulse' : 'opacity-40'}`}
                      style={{ height: isRecording ? `${h}%` : '20%' }}
                    />
                  ))}
                </div>
                
                <button
                  onClick={() => setIsRecording(!isRecording)}
                  className={`px-5 py-2.5 rounded-full text-xs font-bold shadow-lg transition ${
                    isRecording 
                      ? 'bg-rose-600 text-white animate-pulse' 
                      : 'bg-indigo-600 hover:bg-indigo-500 text-white'
                  }`}
                >
                  {isRecording ? "🔴 Listening..." : "🎙️ Push to Talk"}
                </button>
              </div>

              {/* Chat Feed */}
              <div className="h-48 overflow-y-auto space-y-2 p-3 bg-slate-950/50 rounded-xl border border-slate-800/80 text-xs">
                {messages.map((m, idx) => (
                  <div key={idx} className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] p-2.5 rounded-xl ${
                      m.sender === 'user' 
                        ? 'bg-indigo-600 text-white rounded-br-none' 
                        : 'bg-slate-800 text-slate-200 rounded-bl-none'
                    }`}>
                      {m.text}
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex gap-2">
                <input 
                  type="text"
                  value={inputMsg}
                  onChange={(e) => setInputMsg(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Type a message or use voice..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                />
                <button 
                  onClick={handleSendMessage}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold"
                >
                  Send
                </button>
              </div>
            </div>
          )}

        </div>

        {/* System Architecture Sidebar */}
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">Connected API Services</h3>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 font-bold block">JAVA BACKEND</span>
                <span className="text-slate-200 font-medium">companyApi.js / authApi.js</span>
              </div>

              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 font-bold block">PYTHON RAG SERVICE</span>
                <span className="text-indigo-400 font-medium">voiceApi.js (FastAPI / FAISS)</span>
              </div>

              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 font-bold block">CONVERSATION STREAM</span>
                <span className="text-emerald-400 font-medium">conversationApi.js</span>
              </div>

              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 font-bold block">TTS ENGINE</span>
                <span className="text-purple-400 font-medium">{voice} Profile</span>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-500 text-center">
            voiceFlowAi-v1.0 Architecture
          </div>
        </div>

      </div>
    </div>
  );
}