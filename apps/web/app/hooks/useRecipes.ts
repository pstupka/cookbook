import { useEffect, useState } from "react";
import type { components } from "@cookbook/shared/api";
import { api } from "../services/api";
import { useAuthStore } from "../store/auth";

type Recipe = components["schemas"]["RecipeRead"];

export function useRecipes() {
  const { token } = useAuthStore();
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    api
      .get<Recipe[]>("/api/v1/recipes", token ?? undefined)
      .then(setRecipes)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { recipes, loading, error };
}

export function useRecipe(recipeId: string | undefined) {
  const { token } = useAuthStore();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!recipeId) {
      setLoading(false);
      return;
    }
    setLoading(true);
    api
      .get<Recipe>(`/api/v1/recipes/${recipeId}`, token ?? undefined)
      .then(setRecipe)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [recipeId, token]);

  return { recipe, loading, error };
}
