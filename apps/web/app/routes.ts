import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("recipes", "routes/recipes/index.tsx"),
  route("recipes/new", "routes/recipes/new.tsx"),
  route("recipes/:recipeId", "routes/recipes/$recipeId.tsx"),
  route("auth/login", "routes/auth/login.tsx"),
  route("auth/register", "routes/auth/register.tsx"),
  route("ingredients", "routes/ingredients/index.tsx"),
  route("profile", "routes/profile/index.tsx"),
] satisfies RouteConfig;
