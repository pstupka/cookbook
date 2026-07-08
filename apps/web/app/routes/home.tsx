import { Link } from "react-router";

export function meta() {
  return [
    { title: "Cookbook" },
    { name: "description", content: "Your personal recipe collection" },
  ];
}

export default function Home() {
  return (
    <main className="flex-1 flex flex-col items-center justify-center px-4 py-24 text-center">
      <h1 className="text-5xl font-bold tracking-tight text-gray-900 dark:text-white mb-4">
        Your personal cookbook
      </h1>
      <p className="text-lg text-gray-500 dark:text-gray-400 max-w-lg mb-8">
        Save, organize, and share your favourite recipes — all in one place.
      </p>
      <div className="flex gap-4">
        <Link
          to="/recipes"
          className="px-6 py-3 rounded-lg bg-gray-900 text-white font-medium hover:bg-gray-700 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-200 transition-colors"
        >
          Browse recipes
        </Link>
        <Link
          to="/auth/register"
          className="px-6 py-3 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        >
          Get started
        </Link>
      </div>
    </main>
  );
}
