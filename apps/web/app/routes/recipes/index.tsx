import { Link } from "react-router";
import { useRecipes } from "../../hooks/useRecipes";
import { RecipeCard } from "../../components/recipes/RecipeCard";
import { useAuthStore } from "../../store/auth";

export function meta() {
  return [{ title: "Recipes — Cookbook" }];
}

export default function RecipesIndex() {
  const { recipes, loading, error } = useRecipes();
  const { user } = useAuthStore();

  return (
    <main className="max-w-4xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-8">
        {!loading && <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Recipes</h1>}
        {user && (
          <Link
            to="/recipes/new"
            className="px-4 py-2 rounded-lg bg-gray-900 text-white text-sm font-medium hover:bg-gray-700 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-200 transition-colors"
          >
            + New recipe
          </Link>
        )}
      </div>

      {loading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-32 rounded-xl bg-gray-100 dark:bg-gray-800 animate-pulse" />
          ))}
        </div>
      )}

      {error && <p className="text-red-500 dark:text-red-400">Failed to load recipes: {error}</p>}

      {!loading && !error && recipes.length === 0 && (
        <p className="text-gray-500 dark:text-gray-400">No recipes yet.</p>
      )}

      {!loading && !error && recipes.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {recipes.map((recipe) => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      )}
    </main>
  );
}
