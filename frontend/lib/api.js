const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

const tokenKey = "rakshak_access_token";

export function getToken() {
  if (typeof window === "undefined") return "";
  return window.localStorage.getItem(tokenKey) || "";
}

export function setToken(token) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(tokenKey, token);
}

export async function apiRequest(path, options = {}) {
  const token = getToken();
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
    cache: "no-store",
  });

  const text = await response.text();
  const payload = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw new Error(payload.detail || "Request failed");
  }
  return payload;
}

export async function postJson(path, body) {
  return apiRequest(path, {
    method: "POST",
    body: JSON.stringify(body),
  });
}
