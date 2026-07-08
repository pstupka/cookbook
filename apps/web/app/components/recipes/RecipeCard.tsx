import { Link } from "react-router";
import type { components } from "@cookbook/shared/api";
import { Badge } from "../ui/Badge";

type Props = {
  recipe: components["schemas"]["RecipeRead"];
};

export function RecipeCard({ recipe }: Props) {
  return (
    <Link
      to={`/recipes/${recipe.id}`}
      className="block rounded-xl border border-gray-200 dark:border-gray-700 p-5 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
    >
      <div className="flex items-start justify-between gap-2 mb-1">
        <span className="font-semibold text-gray-900 dark:text-white">{recipe.name}</span>
        {recipe.visibility !== "public" && (
          <Badge variant={recipe.visibility === "private" ? "warning" : "default"}>
            {recipe.visibility}
          </Badge>
        )}
      </div>
      {recipe.description && (
        <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 mb-3">
          {recipe.description}
        </p>
      )}
      {recipe.tags.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {recipe.tags.map((tag) => (
            <Badge key={tag.id}>{tag.name}</Badge>
          ))}
        </div>
      )}
    </Link>
  );
}
