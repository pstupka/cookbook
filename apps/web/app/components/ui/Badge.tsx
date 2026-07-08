type Props = {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "danger";
};

export function Badge({ children, variant = "default" }: Props) {
  return <span className={`badge badge-${variant}`}>{children}</span>;
}
