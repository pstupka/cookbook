import { useParams } from "react-router";

export default function EditRecipe() {
  const { recipeId } = useParams();
  return <div>Edit Recipe {recipeId}</div>;
}
