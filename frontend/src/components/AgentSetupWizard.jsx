import React, { useState } from 'react';

export default function AgentSetupWizard() {
  const [step, setStep] = useState(1);
  const [agentName, setAgentName] = useState('VoiceFlow Assistant');
  const [agentType, setAgentType] = useState('Customer Support');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isVectorizing, setIsVectorizing] = useState(false);
  const [indexingComplete, setIndexingComplete] = useState(false);

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      setUploadedFiles(files);
      setIndexingComplete(false);
    }
  };

  const handleStartIndexing = () => {
    if (uploadedFiles.length === 0) return;
    setIsVectorizing(true);
    // Simulate indexing & vectorizing embeddings
    setTimeout(() => {
      setIsVectorizing(false);
      setIndexingComplete(true);
    }, 2000);
  };

  return (
    <div style={{ maxWidth: '700px', margin: '0 auto' }}>
      {/* Wizard Progress Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', borderBottom: '1px solid #e2e8f0', paddingBottom: '1rem' }}>
        <span style={{ fontWeight: step === 1 ? 'bold' : 'normal', color: step === 1 ? '#2563eb' : '#64748b' }}>
          1. Agent Configuration
        </span>
        <span style={{ fontWeight: step === 2 ? 'bold' : 'normal', color: step === 2 ? '#2563eb' : '#64748b' }}>
          2. Document Knowledge Base
        </span>
        <span style={{ fontWeight: step === 3 ? 'bold' : 'normal', color: step === 3 ? '#2563eb' : '#64748b' }}>
          3. Deployment
        </span>
      </div>

      {/* Step 1: Agent Basics */}
      {step === 1 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <h3 style={{ margin: 0, color: '#0f172a' }}>Configure Your AI Agent</h3>
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem', color: '#334155' }}>
              Agent Name
            </label>
            <input
              type="text"
              value={agentName}
              onChange={(e) => setAgentName(e.target.value)}
              style={styles.input}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem', color: '#334155' }}>
              Agent Role / Industry
            </label>
            <select
              value={agentType}
              onChange={(e) => setAgentType(e.target.value)}
              style={styles.input}
            >
              <option>Customer Support</option>
              <option>Appointment Booking</option>
              <option>Order Status & Complaints</option>
            </select>
          </div>
          <button onClick={() => setStep(2)} style={styles.primaryBtn}>
            Next: Knowledge Base & Vectorizing →
          </button>
        </div>
      )}

      {/* Step 2: File Upload & Vector Indexing */}
      {step === 2 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <h3 style={{ margin: 0, color: '#0f172a' }}>Upload & Vectorize Business Knowledge Base</h3>
          <p style={{ margin: 0, color: '#64748b', fontSize: '0.9rem' }}>
            Upload PDFs, text files, or manuals. The system will index and convert the document into semantic vector embeddings for real-time grounded AI answers.
          </p>

          {/* File Picker Box */}
          <div style={styles.dropzone}>
            <input
              type="file"
              accept=".pdf,.txt,.doc,.docx"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              id="file-upload-input"
            />
            <label htmlFor="file-upload-input" style={{ cursor: 'pointer', display: 'block' }}>
              <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📄</div>
              <span style={{ color: '#2563eb', fontWeight: '600' }}>Click here to select files</span>
              <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.8rem' }}>
                Supports PDF, TXT, DOCX
              </p>
            </label>
          </div>

          {/* Uploaded Files Display */}
          {uploadedFiles.length > 0 && (
            <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
              <span style={{ fontSize: '0.875rem', fontWeight: '600', color: '#334155' }}>Selected File:</span>
              <ul style={{ margin: '0.5rem 0 0 0', paddingLeft: '1.25rem', color: '#0f172a', fontSize: '0.9rem' }}>
                {uploadedFiles.map((f, i) => (
                  <li key={i}>{f.name} ({(f.size / 1024).toFixed(1)} KB)</li>
                ))}
              </ul>
            </div>
          )}

          {/* Index / Vectorize Action Button */}
          {uploadedFiles.length > 0 && !indexingComplete && (
            <button
              onClick={handleStartIndexing}
              disabled={isVectorizing}
              style={{ ...styles.primaryBtn, background: isVectorizing ? '#94a3b8' : '#2563eb' }}
            >
              {isVectorizing ? '⚡ Vectorizing & Generating Embeddings...' : 'Start Indexing Document'}
            </button>
          )}

          {/* Indexing Success Message */}
          {indexingComplete && (
            <div style={{ padding: '1rem', background: '#f0fdf4', border: '1px solid #bbf7d0', color: '#166534', borderRadius: '8px', fontSize: '0.9rem' }}>
              ✅ <strong>Vector Indexing Complete!</strong> Document chunks converted to vector embeddings and saved to local vector store.
            </div>
          )}

          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <button onClick={() => setStep(1)} style={styles.secondaryBtn}>
              ← Back
            </button>
            <button onClick={() => setStep(3)} style={styles.primaryBtn}>
              Next: Review & Deploy →
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Confirmation */}
      {step === 3 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <h3 style={{ margin: 0, color: '#0f172a' }}>Agent Ready to Deploy</h3>
          <div style={{ background: '#f8fafc', padding: '1.25rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <p style={{ margin: '0 0 0.5rem 0' }}><strong>Agent Name:</strong> {agentName}</p>
            <p style={{ margin: '0 0 0.5rem 0' }}><strong>Type:</strong> {agentType}</p>
            <p style={{ margin: 0 }}>
              <strong>Knowledge Base Status:</strong> {indexingComplete ? '1 File Indexed (Vectorized)' : 'No Vector Knowledge Base Attached'}
            </p>
          </div>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button onClick={() => setStep(2)} style={styles.secondaryBtn}>
              ← Back
            </button>
            <button onClick={() => alert('Agent deployed! Switch to the Live Voice & Chat Sandbox tab to test.')} style={styles.primaryBtn}>
              🚀 Deploy Agent
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  input: {
    width: '100%',
    padding: '0.75rem 1rem',
    borderRadius: '8px',
    border: '1px solid #cbd5e1',
    fontSize: '0.95rem',
    outline: 'none',
    boxSizing: 'border-box'
  },
  dropzone: {
    border: '2px dashed #cbd5e1',
    borderRadius: '12px',
    padding: '2rem',
    textAlign: 'center',
    background: '#f8fafc',
    transition: 'border 0.2s'
  },
  primaryBtn: {
    padding: '0.75rem 1.5rem',
    background: '#2563eb',
    color: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: '600',
    fontSize: '0.95rem',
    flex: 1
  },
  secondaryBtn: {
    padding: '0.75rem 1.5rem',
    background: '#e2e8f0',
    color: '#334155',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: '600',
    fontSize: '0.95rem'
  }
};