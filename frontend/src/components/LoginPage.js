import { useState } from "react";

const LoginPage = ({ onLogin }) => {
  const [email, setEmail] = useState("default@todo.app");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Login failed. Check your email and password.");
      }

      const data = await response.json();
      onLogin(data.access_token);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-950 px-4">
      <form className="w-full max-w-md rounded-2xl bg-white p-8 shadow-2xl" onSubmit={handleSubmit}>
        <p className="mb-2 text-sm font-bold uppercase tracking-widest text-pink-500">Secure TaskApp</p>
        <h1 className="mb-6 text-3xl font-black text-gray-950">Sign in to your ToDo workspace</h1>

        <label className="mb-2 block text-sm font-semibold text-gray-700" htmlFor="email">
          Email
        </label>
        <input
          id="email"
          className="mb-4 w-full rounded border border-gray-300 p-3 outline-none focus:border-pink-500"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />

        <label className="mb-2 block text-sm font-semibold text-gray-700" htmlFor="password">
          Password
        </label>
        <input
          id="password"
          className="mb-4 w-full rounded border border-gray-300 p-3 outline-none focus:border-pink-500"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />

        {error && <p className="mb-4 rounded bg-red-50 p-3 text-sm font-medium text-red-700">{error}</p>}

        <button
          className="w-full rounded bg-pink-500 px-4 py-3 font-bold text-white hover:bg-pink-600 disabled:cursor-not-allowed disabled:opacity-60"
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Signing in..." : "Login"}
        </button>
      </form>
    </div>
  );
};

export default LoginPage;
