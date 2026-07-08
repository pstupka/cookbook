import type { components } from "@cookbook/shared/api";
import { useAuthStore } from "../store/auth";
import { api } from "../services/api";

type User = components["schemas"]["UserRead"];

export function useAuth() {
  const { user, token, setAuth, clearAuth } = useAuthStore();

  async function login(username: string, password: string) {
    const body = new URLSearchParams({ username, password });
    const data = await api.post<{ access_token: string; token_type: string }>(
      "/api/v1/auth/token",
      body,
    );
    const me = await api.get<User>("/api/v1/users/me", data.access_token);
    setAuth(me, data.access_token);
  }

  function logout() {
    clearAuth();
  }

  return { user, token, login, logout };
}
