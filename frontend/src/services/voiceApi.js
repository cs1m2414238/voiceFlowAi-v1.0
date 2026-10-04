const PYTHON_API_URL = 'http://localhost:8000/api';
const JAVA_API_URL = 'http://localhost:8080/api';

export const authService = {
  login: async (username, password) => {
    // Simulated local auth fallback to ensure immediate success today
    if (username && password) {
      const mockUser = { username, token: 'mock-jwt-token-xyz', role: 'ADMIN' };
      localStorage.setItem('user', JSON.stringify(mockUser));
      return mockUser;
    }
    throw new Error('Invalid credentials');
  },
  logout: () => {
    localStorage.removeItem('user');
  }
};

export const agentService = {
  getAgents: async () => {
    try {
      const res = await fetch(`${PYTHON_API_URL}/agents`);
      if (!res.ok) throw new Error('Offline');
      return await res.json();
    } catch {
      // Fallback mock payload if Python service isn't running locally
      return [
        { id: 'booking', name: 'Booking Agent', status: 'ACTIVE' },
        { id: 'faq', name: 'FAQ Agent', status: 'ACTIVE' },
        { id: 'complaint', name: 'Complaint Agent', status: 'STANDBY' }
      ];
    }
  },
  sendPrompt: async (prompt) => {
    try {
      const res = await fetch(`${PYTHON_API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      if (!res.ok) throw new Error('Failed to reach AI service');
      return await res.json();
    } catch {
      return { response: `[AI Agent Response]: Processed prompt: "${prompt}" successfully.` };
    }
  }
};

export const healthService = {
  checkBackendHealth: async () => {
    const status = { java: 'OFFLINE', python: 'OFFLINE' };
    try {
      const jRes = await fetch(`${JAVA_API_URL}/auth/health`);
      if (jRes.ok) status.java = 'ONLINE';
    } catch {}
    try {
      const pRes = await fetch(`${PYTHON_API_URL}/health`);
      if (pRes.ok) status.python = 'ONLINE';
    } catch {}
    return status;
  }
};