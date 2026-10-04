const TOKEN_KEY = 'vf_token';
const USER_KEY = 'vf_user';

export function getAuthHeaders(extraHeaders = {}) {
  const token = localStorage.getItem(TOKEN_KEY);
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...extraHeaders,
  };
}

export async function login(credentials) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: credentials.email,
      password: credentials.password,
    }),
  });

  if (!response.ok) {
    const errText = await response.text().catch(() => 'Invalid credentials');
    throw new Error(errText || `Login failed (${response.status})`);
  }

  const data = await response.json();
  if (data.token) {
    localStorage.setItem(TOKEN_KEY, data.token);
  }
  localStorage.setItem(USER_KEY, JSON.stringify(data));
  return data;
}

export async function register(userData) {
  const payload = {
    userName: userData.userName || userData.name,
    email: userData.email,
    password: userData.password,
    role: userData.role || 'COMPANY_ADMIN',
    companyId: userData.companyId,
  };

  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errText = await response.text().catch(() => 'Registration failed');
    throw new Error(errText || `Registration failed (${response.status})`);
  }

  const data = await response.json();
  if (data.token) {
    localStorage.setItem(TOKEN_KEY, data.token);
  }
  localStorage.setItem(USER_KEY, JSON.stringify(data));
  return data;
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function getCurrentUser() {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function setCurrentUser(user) {
  if (!user) {
    logout();
    return;
  }
  if (user.token) {
    localStorage.setItem(TOKEN_KEY, user.token);
  }
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}
