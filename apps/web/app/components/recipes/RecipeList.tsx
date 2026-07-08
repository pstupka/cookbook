import type { components } from "@cookbook/shared/api";
import { RecipeCard } from "./RecipeCard";

type Props = {
  recipes: components["schemas"]["RecipeRead"][];
};

export function RecipeList({ recipes }: Props) {
  if (recipes.length === 0) return <p>No recipes found.</p>;
  return (
    <div>
      {recipes.map((recipe) => (
        <RecipeCard key={recipe.id} recipe={recipe} />
      ))}
    </div>
  );
}
