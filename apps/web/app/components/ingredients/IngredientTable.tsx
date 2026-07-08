import type { components } from "@cookbook/shared/api";

type Props = {
  ingredients: components["schemas"]["IngredientRead"][];
  onDelete: (id: number) => void;
};

export function IngredientTable({ ingredients, onDelete }: Props) {
  if (ingredients.length === 0) return <p>No ingredients.</p>;
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Default unit</th>
          <th />
        </tr>
      </thead>
      <tbody>
        {ingredients.map((ing) => (
          <tr key={ing.id}>
            <td>{ing.name}</td>
            <td>{ing.default_unit ?? "—"}</td>
            <td>
              <button onClick={() => onDelete(ing.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
