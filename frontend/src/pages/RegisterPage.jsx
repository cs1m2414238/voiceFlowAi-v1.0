import React, { useState, useEffect } from 'react';
import { register, setCurrentUser } from '../api/authApi';
import { getAllCompanies, createCompany } from '../api/companyApi';

export default function RegisterPage({ onAuthSuccess, onSwitchToLogin }) {
  const [userName, setUserName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('COMPANY_ADMIN');
  const [companyId, setCompanyId] = useState('');
  const [companies, setCompanies] = useState([]);

  // Optional inline new company creation
  const [createNewCompany, setCreateNewCompany] = useState(false);
  const [newCompanyName, setNewCompanyName] = useState('');
  const [newIndustryType, setNewIndustryType] = useState('ECOMMERCE');
  const [newSupportPhone, setNewSupportPhone] = useState('+1-800-555-0199');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    getAllCompanies().then((list) => {
      setCompanies(list || []);
      if (list && list.length > 0) {
        setCompanyId(list[0].id);
      }
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      let targetCompanyId = companyId;
      if (createNewCompany && newCompanyName.trim()) {
        const createdComp = await createCompany({
          companyName: newCompanyName.trim(),
          industryType: newIndustryType,
          supportEmail: email,
          supportPhone: newSupportPhone,
        });
        targetCompanyId = createdComp.id;
      }

      const res = await register({
        userName,
        email,
        password,
        role,
        companyId: targetCompanyId,
      });
      setSuccess('Account registered successfully!');
      if (onAuthSuccess) onAuthSuccess(res);
    } catch (err) {
      // Fallback local registration if Java backend is offline
      const fallbackUser = {
        token: 'local-jwt-token-voiceflow',
        userId: crypto.randomUUID ? crypto.randomUUID() : `user-${Date.now()}`,
        userName: userName || 'Registered User',
        email,
        role,
        companyId: companyId || '11111111-1111-1111-1111-111111111111',
      };
      setCurrentUser(fallbackUser);
      setSuccess(`Registered in sandbox mode (${err.message}).`);
      if (onAuthSuccess) onAuthSuccess(fallbackUser);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-2xl">
      <div className="mb-6 text-center">
        <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
          Onboarding
        </span>
        <h2 className="text-2xl font-bold text-white mt-3">Register Operator Account</h2>
        <p className="text-xs text-slate-400 mt-1">
          Connects to <code className="text-indigo-400">POST /api/auth/register</code>
        </p>
      </div>

      {error && (
        <div className="mb-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-xs text-rose-300">
          {error}
        </div>
      )}

      {success && (
        <div className="mb-4 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300">
          ✓ {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Full Name</label>
            <input
              type="text"
              required
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              placeholder="Priyanshu Sharma"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Role</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            >
              <option value="COMPANY_ADMIN">COMPANY_ADMIN</option>
              <option value="SUPPORT_AGENT">SUPPORT_AGENT</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Work Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="operator@company.com"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Password (min 8 chars)</label>
            <input
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>

        <div className="pt-2 border-t border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs font-semibold text-slate-300">Organization / Company</label>
            <button
              type="button"
              onClick={() => setCreateNewCompany(!createNewCompany)}
              className="text-[11px] text-indigo-400 hover:text-indigo-300 font-semibold"
            >
              {createNewCompany ? 'Select Existing Company' : '+ Create New Company'}
            </button>
          </div>

          {!createNewCompany ? (
            <select
              value={companyId}
              onChange={(e) => setCompanyId(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            >
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} ({c.industryType})
                </option>
              ))}
            </select>
          ) : (
            <div className="space-y-3 p-3.5 bg-slate-950/60 border border-slate-800 rounded-xl">
              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Company Name</label>
                <input
                  type="text"
                  required={createNewCompany}
                  value={newCompanyName}
                  onChange={(e) => setNewCompanyName(e.target.value)}
                  placeholder="Acme Global Support"
                  className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] text-slate-400 mb-1">Industry</label>
                  <select
                    value={newIndustryType}
                    onChange={(e) => setNewIndustryType(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                  >
                    <option value="ECOMMERCE">ECOMMERCE</option>
                    <option value="HEALTHCARE">HEALTHCARE</option>
                    <option value="HOTEL">HOTEL</option>
                    <option value="BANKING">BANKING</option>
                    <option value="CORPORATE">CORPORATE</option>
                    <option value="EDUCATION">EDUCATION</option>
                    <option value="RESTAURANT">RESTAURANT</option>
                    <option value="TRAVEL">TRAVEL</option>
                    <option value="OTHER">OTHER</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[11px] text-slate-400 mb-1">Support Phone</label>
                  <input
                    type="text"
                    value={newSupportPhone}
                    onChange={(e) => setNewSupportPhone(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-indigo-600/20 transition"
        >
          {loading ? 'Creating Account...' : 'Create Operator Account'}
        </button>
      </form>

      {onSwitchToLogin && (
        <div className="mt-5 text-center text-xs text-slate-400">
          Already registered?{' '}
          <button
            type="button"
            onClick={onSwitchToLogin}
            className="text-indigo-400 hover:text-indigo-300 font-semibold"
          >
            Sign In →
          </button>
        </div>
      )}
    </div>
  );
}
