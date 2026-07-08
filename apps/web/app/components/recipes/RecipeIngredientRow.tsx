import type { components } from "@cookbook/shared/api";

type Props = {
  ingredient: components["schemas"]["RecipeIngredientRead"];
};

export function RecipeIngredientRow({ ingredient }: Props) {
  return (
    <tr>
      <td>{ingredient.ingredient.name}</td>
      <td>{ingredient.quantity}</td>
      <td>{ingredient.unit ?? "—"}</td>
    </tr>
  );
}
