const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(
  method: string,
  path: string,
  token?: string,
  body?: unknown,
): Promise<T> {
  const isFormData = body instanceof URLSearchParams;
  const headers: Record<string, string> = {};

  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (body && !isFormData) headers["Content-Type"] = "application/json";

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: isFormData ? body : body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string, token?: string) => request<T>("GET", path, token),
  post: <T>(path: string, body: unknown, token?: string) => request<T>("POST", path, token, body),
  put: <T>(path: string, body: unknown, token?: string) => request<T>("PUT", path, token, body),
  patch: <T>(path: string, body: unknown, token?: string) => request<T>("PATCH", path, token, body),
  delete: <T>(path: string, token?: string) => request<T>("DELETE", path, token),
};
