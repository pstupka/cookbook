import type { components } from "@cookbook/shared/api";

type Props = {
  step: components["schemas"]["RecipeStep"];
};

export function RecipeStepRow({ step }: Props) {
  return (
    <li>
      <span>{step.order}.</span>
      <span>{step.text}</span>
      {step.photo_url && <img src={step.photo_url} alt={`Step ${step.order}`} />}
    </li>
  );
}
