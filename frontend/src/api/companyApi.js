import { getAuthHeaders } from './authApi';

const FALLBACK_COMPANIES_KEY = 'vf_companies_fallback';

const DEFAULT_COMPANIES = [
  {
    id: '11111111-1111-1111-1111-111111111111',
    name: 'NovaMart E-Commerce',
    industryType: 'ECOMMERCE',
    supportEmail: 'support@novamart.io',
    supportPhone: '+1-800-555-0191',
    active: true,
    createdAt: '2026-01-15T09:00:00',
  },
  {
    id: '22222222-2222-2222-2222-222222222222',
    name: 'Apex Care Medical Clinic',
    industryType: 'HEALTHCARE',
    supportEmail: 'care@apexmedical.org',
    supportPhone: '+1-800-555-0144',
    active: true,
    createdAt: '2026-01-18T11:30:00',
  },
  {
    id: '33333333-3333-3333-3333-333333333333',
    name: 'Grand Horizon Hotels',
    industryType: 'HOTEL',
    supportEmail: 'concierge@grandhorizon.com',
    supportPhone: '+1-800-555-0178',
    active: true,
    createdAt: '2026-01-20T14:15:00',
  },
];

function getLocalCompanies() {
  try {
    const raw = localStorage.getItem(FALLBACK_COMPANIES_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    // ignore storage errors
  }
  localStorage.setItem(FALLBACK_COMPANIES_KEY, JSON.stringify(DEFAULT_COMPANIES));
  return DEFAULT_COMPANIES;
}

function saveLocalCompanies(list) {
  try {
    localStorage.setItem(FALLBACK_COMPANIES_KEY, JSON.stringify(list));
  } catch {
    // ignore storage errors
  }
}

export async function createCompany(data) {
  const payload = {
    companyName: data.companyName || data.name,
    industryType: data.industryType || 'ECOMMERCE',
    supportEmail: data.supportEmail || '',
    supportPhone: data.supportPhone || '+1-800-000-0000',
  };

  try {
    const response = await fetch('/api/companies', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Failed to create company (${response.status})`);
    }
    return await response.json();
  } catch {
    const created = {
      id: crypto.randomUUID ? crypto.randomUUID() : `comp-${Date.now()}`,
      name: payload.companyName,
      industryType: payload.industryType,
      supportEmail: payload.supportEmail,
      supportPhone: payload.supportPhone,
      active: true,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    const list = [created, ...getLocalCompanies()];
    saveLocalCompanies(list);
    return created;
  }
}

export async function getAllCompanies() {
  try {
    const response = await fetch('/api/companies', {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch companies (${response.status})`);
    }
    return await response.json();
  } catch {
    return getLocalCompanies();
  }
}

export async function getCompanyById(id) {
  try {
    const response = await fetch(`/api/companies/${id}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error(`Company ${id} not found (${response.status})`);
    }
    return await response.json();
  } catch {
    return getLocalCompanies().find((c) => c.id === id) || null;
  }
}

export async function updateCompany(id, data) {
  const payload = {
    companyName: data.companyName || data.name,
    industryType: data.industryType,
    supportEmail: data.supportEmail,
    supportPhone: data.supportPhone,
    active: data.active,
  };

  try {
    const response = await fetch(`/api/companies/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(`Failed to update company (${response.status})`);
    }
    return await response.json();
  } catch {
    const list = getLocalCompanies().map((c) =>
      c.id === id
        ? {
            ...c,
            name: payload.companyName ?? c.name,
            industryType: payload.industryType ?? c.industryType,
            supportEmail: payload.supportEmail ?? c.supportEmail,
            supportPhone: payload.supportPhone ?? c.supportPhone,
            active: payload.active ?? c.active,
            updatedAt: new Date().toISOString(),
          }
        : c
    );
    saveLocalCompanies(list);
    return list.find((c) => c.id === id);
  }
}

export async function deleteCompany(id) {
  try {
    const response = await fetch(`/api/companies/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error(`Failed to delete company (${response.status})`);
    }
    return true;
  } catch {
    const list = getLocalCompanies().filter((c) => c.id !== id);
    saveLocalCompanies(list);
    return true;
  }
}
