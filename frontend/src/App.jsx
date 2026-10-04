import React, { useState, useEffect } from 'react';
import AgentSetupWizard from './components/AgentSetupWizard';
import { authService, agentService, healthService } from './services/voiceApi';

export default function App() {
  const [showWelcome, setShowWelcome] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [activeTab, setActiveTab] = useState('wizard');
  const [health, setHealth] = useState({ java: 'UNKNOWN', python: 'UNKNOWN' });
  const [prompt, setPrompt] = useState('');
  const [chatLog, setChatLog] = useState([]);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setIsLoggedIn(true);
      setShowWelcome(false);
    }
  }, []);

  useEffect(() => {
    if (isLoggedIn) {
      healthService.checkBackendHealth().then(setHealth);
    }
  }, [isLoggedIn]);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await authService.login(username, password);
      setIsLoggedIn(true);
      setShowWelcome(false);
    } catch (err) {
      alert(err.message);
    }
  };

  const handleLogout = () => {
    authService.logout();
    setIsLoggedIn(false);
    setShowWelcome(true);
  };

  const handleSendPrompt = async () => {
    if (!prompt) return;
    const userMsg = prompt;
    setChatLog((prev) => [...prev, { sender: 'Customer', text: userMsg }]);
    setPrompt('');
    const res = await agentService.sendPrompt(userMsg);
    setChatLog((prev) => [...prev, { sender: 'AI Agent', text: res.response }]);
  };

  // 1. WELCOME / LANDING PAGE
  if (showWelcome && !isLoggedIn) {
    return (
      <div style={styles.welcomeContainer}>
        <header style={styles.welcomeHeader}>
          <h2 style={{ color: '#2563eb', margin: 0 }}>VoiceFlow AI</h2>
          <button onClick={() => setShowWelcome(false)} style={styles.button}>
            Portal Login
          </button>
        </header>

        <main style={styles.heroSection}>
          <span style={styles.badge}>Next-Gen AI Customer Automation</span>
          <h1 style={styles.heroTitle}>Deploy Voice & AI Agents for Your Business</h1>
          <p style={styles.heroSubtitle}>
            Automate customer inquiries, streamline document verification, and deliver real-time intelligent voice assistance tailored to your enterprise.
          </p>

          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <button onClick={() => setShowWelcome(false)} style={styles.heroPrimaryBtn}>
              Get Started Now
            </button>
          </div>

          <div style={styles.featureGrid}>
            <div style={styles.featureCard}>
              <h3 style={{ color: '#0f172a' }}>⚡ Instant Agent Setup</h3>
              <p style={{ color: '#64748b', fontSize: '0.9rem' }}>
                Configure and deploy customized booking, FAQ, and support agents in minutes.
              </p>
            </div>
            <div style={styles.featureCard}>
              <h3 style={{ color: '#0f172a' }}>📄 Smart RAG Verification</h3>
              <p style={{ color: '#64748b', fontSize: '0.9rem' }}>
                Upload business knowledge bases and documents for precise, grounded answers.
              </p>
            </div>
            <div style={styles.featureCard}>
              <h3 style={{ color: '#0f172a' }}>🎙️ Live Sandbox Testing</h3>
              <p style={{ color: '#64748b', fontSize: '0.9rem' }}>
                Test speech-to-text and chat capabilities in real-time before going live.
              </p>
            </div>
          </div>
        </main>
      </div>
    );
  }

  // 2. LOGIN PAGE
  if (!isLoggedIn) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <button 
            onClick={() => setShowWelcome(true)} 
            style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', float: 'left', fontSize: '0.85rem' }}
          >
            ← Back
          </button>
          <div style={{ clear: 'both' }}></div>
          <h2 style={{ color: '#2563eb', marginBottom: '0.5rem', marginTop: '0.5rem' }}>VoiceFlow Business Portal</h2>
          <p style={{ color: '#64748b', fontSize: '0.875rem' }}>Sign in to configure your automated AI agent</p>
          <form onSubmit={handleLogin} style={styles.form}>
            <input
              type="text"
              placeholder="Business Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={styles.input}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
              required
            />
            <button type="submit" style={styles.button}>Sign In</button>
          </form>
        </div>
      </div>
    );
  }

  // 3. MAIN PORTAL DASHBOARD
  return (
    <div style={styles.dashboard}>
      <header style={styles.header}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.25rem', color: '#0f172a' }}>VoiceFlow AI Portal</h1>
          <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Enterprise Agent Management</span>
        </div>
        <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
      </header>

      <nav style={styles.nav}>
        <button
          style={activeTab === 'wizard' ? styles.activeTab : styles.tab}
          onClick={() => setActiveTab('wizard')}
        >
          Agent Setup & Onboarding
        </button>
        <button
          style={activeTab === 'sandbox' ? styles.activeTab : styles.tab}
          onClick={() => setActiveTab('sandbox')}
        >
          Live Voice & Chat Sandbox
        </button>
        <button
          style={activeTab === 'health' ? styles.activeTab : styles.tab}
          onClick={() => setActiveTab('health')}
        >
          System Telemetry
        </button>
      </nav>

      <main style={styles.main}>
        {activeTab === 'wizard' && (
          <div style={{ background: '#ffffff', borderRadius: '12px', padding: '1.5rem', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
            <AgentSetupWizard />
          </div>
        )}

        {activeTab === 'sandbox' && (
          <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <h3 style={{ color: '#0f172a', marginTop: 0 }}>Test Your Configured Agent</h3>
            <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
              Simulate customer interactions before going live to verify how your AI handles inquiries and document-based questions.
            </p>
            <div style={styles.chatBox}>
              {chatLog.length === 0 ? (
                <p style={{ color: '#94a3b8', textAlign: 'center', marginTop: '4rem' }}>
                  Send a message to test your AI workflow...
                </p>
              ) : (
                chatLog.map((msg, i) => (
                  <div key={i} style={{ marginBottom: '0.75rem' }}>
                    <strong style={{ color: msg.sender === 'Customer' ? '#2563eb' : '#059669' }}>
                      {msg.sender}:
                    </strong>{' '}
                    <span style={{ color: '#334155' }}>{msg.text}</span>
                  </div>
                ))
              )}
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Ask your agent a question..."
                style={styles.input}
                onKeyDown={(e) => e.key === 'Enter' && handleSendPrompt()}
              />
              <button onClick={handleSendPrompt} style={styles.button}>Send</button>
            </div>
          </div>
        )}

        {activeTab === 'health' && (
          <div style={{ maxWidth: '600px', background: '#ffffff', padding: '1.5rem', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
            <h3 style={{ color: '#0f172a', marginTop: 0 }}>System Telemetry & Backend Connections</h3>
            <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={styles.statusRow}>
                <span style={{ fontWeight: '500', color: '#334155' }}>Java Core Backend (Port 8080)</span>
                <span style={{ color: health.java === 'ONLINE' ? '#16a34a' : '#dc2626', fontWeight: 'bold' }}>
                  ● {health.java}
                </span>
              </div>
              <div style={styles.statusRow}>
                <span style={{ fontWeight: '500', color: '#334155' }}>Python AI Service (Port 8000)</span>
                <span style={{ color: health.python === 'ONLINE' ? '#16a34a' : '#dc2626', fontWeight: 'bold' }}>
                  ● {health.python}
                </span>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

const styles = {
  welcomeContainer: { minHeight: '100vh', background: '#f8fafc', color: '#0f172a', display: 'flex', flexDirection: 'column' },
  welcomeHeader: { padding: '1.5rem 3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#ffffff', borderBottom: '1px solid #e2e8f0' },
  heroSection: { flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '4rem 2rem' },
  badge: { background: '#eff6ff', color: '#2563eb', padding: '0.4rem 1rem', borderRadius: '9999px', fontSize: '0.85rem', fontWeight: '600', border: '1px solid #bfdbfe', marginBottom: '1.5rem' },
  heroTitle: { fontSize: '2.75rem', fontWeight: '800', color: '#0f172a', maxWidth: '750px', margin: '0 0 1rem 0', lineHeight: 1.2 },
  heroSubtitle: { fontSize: '1.1rem', color: '#64748b', maxWidth: '600px', lineHeight: 1.6, margin: '0 0 1.5rem 0' },
  heroPrimaryBtn: { padding: '0.9rem 2rem', background: '#2563eb', color: '#ffffff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '1rem', boxShadow: '0 4px 14px rgba(37, 99, 235, 0.3)' },
  featureGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem', maxWidth: '900px', width: '100%', marginTop: '4rem' },
  featureCard: { background: '#ffffff', padding: '1.5rem', borderRadius: '12px', border: '1px solid #e2e8f0', textAlign: 'left', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' },
  
  container: { height: '100vh', background: '#f8fafc', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#0f172a' },
  card: { background: '#ffffff', padding: '2.5rem', borderRadius: '12px', width: '350px', textAlign: 'center', boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)', border: '1px solid #e2e8f0' },
  form: { display: 'flex', flexDirection: 'column', gap: '1.25rem', marginTop: '1.5rem' },
  input: { padding: '0.85rem 1rem', borderRadius: '8px', border: '1px solid #cbd5e1', background: '#ffffff', color: '#0f172a', width: '100%', boxSizing: 'border-box', outline: 'none', fontSize: '0.95rem' },
  button: { padding: '0.85rem 1.25rem', background: '#2563eb', color: '#ffffff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '0.95rem', boxShadow: '0 4px 12px rgba(37, 99, 235, 0.2)' },
  
  dashboard: { minHeight: '100vh', background: '#f8fafc', color: '#0f172a', display: 'flex', flexDirection: 'column' },
  header: { padding: '1.25rem 2.5rem', background: '#ffffff', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #e2e8f0' },
  logoutBtn: { background: '#ef4444', color: '#ffffff', border: 'none', padding: '0.5rem 1.25rem', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '0.875rem' },
  nav: { display: 'flex', background: '#ffffff', borderBottom: '1px solid #e2e8f0', padding: '0 2.5rem', gap: '0.5rem' },
  tab: { background: 'none', border: 'none', color: '#64748b', padding: '1rem 1.5rem', cursor: 'pointer', fontSize: '0.95rem', fontWeight: '500', transition: 'all 0.2s' },
  activeTab: { background: '#f8fafc', border: 'none', color: '#2563eb', padding: '1rem 1.5rem', cursor: 'pointer', fontSize: '0.95rem', fontWeight: '600', borderBottom: '3px solid #2563eb' },
  main: { padding: '2.5rem', flex: 1 },
  chatBox: { background: '#ffffff', padding: '1.5rem', height: '340px', overflowY: 'auto', borderRadius: '12px', marginBottom: '1.25rem', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' },
  statusRow: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 1.25rem', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }
};