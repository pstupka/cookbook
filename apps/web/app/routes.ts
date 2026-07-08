import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("recipes", "routes/recipes/index.tsx"),
  route("recipes/:recipeId", "routes/recipes/$recipeId.tsx"),
  route("auth/login", "routes/auth/login.tsx"),
] satisfies RouteConfig;
