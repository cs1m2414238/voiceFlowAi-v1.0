import React, { useState } from 'react';
import { login, setCurrentUser } from '../api/authApi';

export default function LoginPage({ onAuthSuccess, onSwitchToRegister }) {
  const [email, setEmail] = useState('admin@novamart.io');
  const [password, setPassword] = useState('VoiceFlow@2026');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [statusMsg, setStatusMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setStatusMsg('');

    try {
      const user = await login({ email, password });
      setStatusMsg('Authenticated via Java Backend JWT.');
      if (onAuthSuccess) onAuthSuccess(user);
    } catch (err) {
      setError(`Backend login unavailable (${err.message}). You can use Demo Login below.`);
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (role = 'COMPANY_ADMIN') => {
    const demoUser = {
      token: 'demo-jwt-token-voiceflow-2026',
      userId: 'aaaa1111-1111-1111-1111-111111111111',
      userName: role === 'COMPANY_ADMIN' ? 'Priyanshu (Admin)' : 'Support Specialist',
      email: email || 'admin@novamart.io',
      role,
      companyId: '11111111-1111-1111-1111-111111111111',
    };
    setCurrentUser(demoUser);
    setStatusMsg(`Signed in as ${demoUser.userName} (${role})`);
    if (onAuthSuccess) onAuthSuccess(demoUser);
  };

  return (
    <div className="max-w-md mx-auto bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-2xl">
      <div className="mb-6 text-center">
        <span className="text-xs font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/20">
          JWT Authentication
        </span>
        <h2 className="text-2xl font-bold text-white mt-3">Sign in to VoiceFlow AI</h2>
        <p className="text-xs text-slate-400 mt-1">
          Connects to <code className="text-indigo-400">POST /api/auth/login</code> on Java Backend
        </p>
      </div>

      {error && (
        <div className="mb-4 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300">
          ⚠️ {error}
        </div>
      )}

      {statusMsg && (
        <div className="mb-4 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300">
          ✓ {statusMsg}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-1">Work Email</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="admin@company.com"
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-xl text-xs font-bold shadow-lg shadow-indigo-600/20 transition"
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <div className="mt-6 pt-5 border-t border-slate-800">
        <p className="text-[11px] text-slate-400 text-center mb-3">Quick Demo Access (Offline / Sandbox Mode)</p>
        <div className="grid grid-cols-2 gap-2">
          <button
            type="button"
            onClick={() => handleDemoLogin('COMPANY_ADMIN')}
            className="py-2 px-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold border border-slate-700 transition"
          >
            🛡️ Demo Admin
          </button>
          <button
            type="button"
            onClick={() => handleDemoLogin('SUPPORT_AGENT')}
            className="py-2 px-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold border border-slate-700 transition"
          >
            🎧 Support Agent
          </button>
        </div>
      </div>

      {onSwitchToRegister && (
        <div className="mt-5 text-center text-xs text-slate-400">
          Don&apos;t have an account?{' '}
          <button
            type="button"
            onClick={onSwitchToRegister}
            className="text-indigo-400 hover:text-indigo-300 font-semibold"
          >
            Register User &amp; Company →
          </button>
        </div>
      )}
    </div>
  );
}
