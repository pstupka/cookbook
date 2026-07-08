import type { components } from "@cookbook/shared/api";
import { Input } from "../ui/Input";
import { Select } from "../ui/Select";

const UNIT_OPTIONS: { label: string; value: components["schemas"]["IngredientUnit"] }[] = [
  { label: "g", value: "g" },
  { label: "kg", value: "kg" },
  { label: "ml", value: "ml" },
  { label: "l", value: "l" },
  { label: "cup", value: "cup" },
  { label: "tbsp", value: "tbsp" },
  { label: "tsp", value: "tsp" },
  { label: "pc", value: "pc" },
];

type Props = {
  onSubmit: (data: components["schemas"]["IngredientCreate"]) => void;
};

export function IngredientForm({ onSubmit }: Props) {
  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    onSubmit({
      name: form.get("name") as string,
      default_unit: (form.get("default_unit") as components["schemas"]["IngredientUnit"]) || null,
    });
    e.currentTarget.reset();
  }

  return (
    <form onSubmit={handleSubmit}>
      <Input label="Name" id="name" name="name" required />
      <Select label="Default unit" id="default_unit" name="default_unit" options={UNIT_OPTIONS} />
      <button type="submit">Add</button>
    </form>
  );
}
