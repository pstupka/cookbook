import { useEffect, useState } from "react";
import type { components } from "@cookbook/shared/api";
import { api } from "../services/api";
import { useAuthStore } from "../store/auth";

type Ingredient = components["schemas"]["IngredientRead"];

export function useIngredients() {
  const { token } = useAuthStore();
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    api
      .get<Ingredient[]>("/api/v1/ingredients", token ?? undefined)
      .then(setIngredients)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { ingredients, loading, error };
}
