import type { SelectHTMLAttributes } from "react";

type Option = { label: string; value: string };

type Props = SelectHTMLAttributes<HTMLSelectElement> & {
  label?: string;
  options: Option[];
  error?: string;
};

export function Select({ label, options, error, id, ...props }: Props) {
  return (
    <div>
      {label && <label htmlFor={id}>{label}</label>}
      <select id={id} {...props}>
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
      {error && <span>{error}</span>}
    </div>
  );
}
