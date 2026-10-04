import React, { useState, useEffect } from 'react';
import { getAllCompanies, createCompany, deleteCompany } from '../api/companyApi';

const INDUSTRIES = [
  'ECOMMERCE',
  'HEALTHCARE',
  'HOTEL',
  'BANKING',
  'CORPORATE',
  'EDUCATION',
  'RESTAURANT',
  'TRAVEL',
  'OTHER',
];

export default function CompanyPage() {
  const [companies, setCompanies] = useState([]);
  const [companyName, setCompanyName] = useState('');
  const [industryType, setIndustryType] = useState('ECOMMERCE');
  const [supportEmail, setSupportEmail] = useState('');
  const [supportPhone, setSupportPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');

  const loadCompanies = async () => {
    const list = await getAllCompanies();
    setCompanies(list || []);
  };

  useEffect(() => {
    loadCompanies();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!companyName.trim()) return;
    setLoading(true);
    setStatusMsg('');

    try {
      const created = await createCompany({
        companyName: companyName.trim(),
        industryType,
        supportEmail: supportEmail.trim() || `support@${companyName.toLowerCase().replace(/\s+/g, '')}.com`,
        supportPhone: supportPhone.trim() || '+1-800-555-0100',
      });
      setCompanies((prev) => [created, ...prev.filter((c) => c.id !== created.id)]);
      setCompanyName('');
      setSupportEmail('');
      setSupportPhone('');
      setStatusMsg(`Created company "${created.name}" (${created.industryType})`);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    await deleteCompany(id);
    setCompanies((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Create Company Form */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl h-fit">
        <span className="text-xs font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/20">
          Tenant Management
        </span>
        <h2 className="text-xl font-bold text-white mt-3">Register Company</h2>
        <p className="text-xs text-slate-400 mt-1 mb-5">
          Calls <code className="text-indigo-400">POST /api/companies</code>
        </p>

        {statusMsg && (
          <div className="mb-4 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300">
            ✓ {statusMsg}
          </div>
        )}

        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Company Name</label>
            <input
              type="text"
              required
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder="e.g. Horizon Airlines"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Industry Vertical</label>
            <select
              value={industryType}
              onChange={(e) => setIndustryType(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            >
              {INDUSTRIES.map((ind) => (
                <option key={ind} value={ind}>
                  {ind}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Support Email</label>
            <input
              type="email"
              required
              value={supportEmail}
              onChange={(e) => setSupportEmail(e.target.value)}
              placeholder="support@company.com"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Support Phone</label>
            <input
              type="text"
              required
              value={supportPhone}
              onChange={(e) => setSupportPhone(e.target.value)}
              placeholder="+1-800-555-0199"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-indigo-600/20 transition"
          >
            {loading ? 'Saving...' : '+ Add Company'}
          </button>
        </form>
      </div>

      {/* Company Directory */}
      <div className="lg:col-span-2 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex justify-between items-center mb-5">
          <div>
            <h3 className="text-lg font-bold text-white">Registered Tenant Organizations</h3>
            <p className="text-xs text-slate-400">
              Each company has an isolated knowledge base namespace (`company_id`)
            </p>
          </div>
          <span className="text-xs font-mono text-slate-400 bg-slate-950 px-3 py-1 rounded-lg border border-slate-800">
            Total: {companies.length}
          </span>
        </div>

        <div className="space-y-3">
          {companies.map((comp) => (
            <div
              key={comp.id}
              className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
            >
              <div>
                <div className="flex items-center gap-2.5">
                  <h4 className="font-bold text-white text-sm">{comp.name}</h4>
                  <span className="px-2.5 py-0.5 text-[10px] font-mono font-semibold rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    {comp.industryType}
                  </span>
                  <span className="px-2 py-0.5 text-[10px] rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {comp.active !== false ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="text-xs text-slate-400 mt-1 flex flex-wrap gap-4">
                  <span>📧 {comp.supportEmail || 'N/A'}</span>
                  <span>📞 {comp.supportPhone || 'N/A'}</span>
                  <span className="font-mono text-[11px] text-slate-500">ID: {comp.id}</span>
                </div>
              </div>

              <button
                onClick={() => handleDelete(comp.id)}
                className="px-3 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 text-xs font-semibold self-start sm:self-center transition"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
