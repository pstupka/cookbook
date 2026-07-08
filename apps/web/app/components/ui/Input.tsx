import type { InputHTMLAttributes } from "react";

type Props = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string;
};

export function Input({ label, error, id, ...props }: Props) {
  return (
    <div>
      {label && <label htmlFor={id}>{label}</label>}
      <input id={id} {...props} />
      {error && <span>{error}</span>}
    </div>
  );
}
