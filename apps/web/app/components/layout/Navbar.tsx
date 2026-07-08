import { Link, NavLink } from "react-router";
import { useAuth } from "../../hooks/useAuth";

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="border-b border-gray-200 dark:border-gray-800 px-6 py-3 flex items-center justify-between">
      <Link to="/" className="font-semibold text-gray-900 dark:text-white">
        Cookbook
      </Link>
      <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
        <NavLink
          to="/recipes"
          className="hover:text-gray-900 dark:hover:text-white transition-colors"
        >
          Recipes
        </NavLink>
        {user && (
          <NavLink
            to="/ingredients"
            className="hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Ingredients
          </NavLink>
        )}
        {user ? (
          <>
            <NavLink
              to="/recipes/new"
              className="hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              New recipe
            </NavLink>
            <NavLink
              to="/profile"
              className="hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Profile
            </NavLink>
            <button
              onClick={logout}
              className="hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <NavLink
              to="/auth/login"
              className="hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Login
            </NavLink>
            <NavLink
              to="/auth/register"
              className="px-3 py-1.5 rounded-md bg-gray-900 text-white dark:bg-white dark:text-gray-900 hover:opacity-80 transition-opacity"
            >
              Register
            </NavLink>
          </>
        )}
      </div>
    </nav>
  );
}
