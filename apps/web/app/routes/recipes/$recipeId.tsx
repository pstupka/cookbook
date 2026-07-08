import { useParams } from "react-router";
import { RecipeCard } from "~/components";
import { useRecipe } from "~/hooks/useRecipes";

export default function RecipeDetail() {
  const { recipeId } = useParams();
  const { recipe, loading, error } = useRecipe(recipeId);

  if (loading) return <p>Loading…</p>;
  if (error) return <p>Error: {error}</p>;
  if (!recipe) return <p>Recipe not found.</p>;

  return (
    <div>
      <RecipeCard key={recipeId} recipe={recipe} />
    </div>
  );
}
