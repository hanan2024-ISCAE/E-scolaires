import { useState } from "react";
import axios from "axios";

export default function Login() {
  // =========================================
  // STATES
  // =========================================
  const [username, setUsername] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  // =========================================
  // LOGIN
  // =========================================
  async function handleLogin(e) {
    e.preventDefault();

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/api/login/",
        {
          username,
          password,
        },
      );

      // =========================================
      // SAVE TOKEN
      // =========================================
      localStorage.setItem(
        "access",
        response.data.access,
      );
      localStorage.setItem(
        "refresh",
        response.data.refresh
      );

      localStorage.setItem(
        "role",
        response.data.role,
      );

      localStorage.setItem(
        "username",
        response.data.username,
      );

      setMessage("✅ Connexion réussie");

      console.log(response.data);

      // =========================================
      // REDIRECTION
      // =========================================
      if (response.data.role === "admin") {

        window.location.href = "/admin";

      } else {

        window.location.href = "/etudiant";

      }

    } catch (error) {

      console.log(error);

      setMessage("❌ Identifiants invalides");

    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-[#0f1117] flex items-center justify-center px-5">
      <div
        className="w-full max-w-md bg-[#161b27]
        border border-[#2d3748]
        rounded-2xl p-8 shadow-2xl"
      >
        {/* ========================================= */}
        {/* TITRE */}
        {/* ========================================= */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">E-Scolaire</h1>

          <p className="text-slate-400">Connectez-vous à votre compte</p>
        </div>

        {/* ========================================= */}
        {/* MESSAGE */}
        {/* ========================================= */}
        {message && (
          <div
            className="mb-5 bg-[#0f1117]
            border border-[#374151]
            text-white text-sm
            rounded-lg p-3"
          >
            {message}
          </div>
        )}

        {/* ========================================= */}
        {/* FORMULAIRE */}
        {/* ========================================= */}
        <form onSubmit={handleLogin} className="space-y-5">
          {/* USERNAME */}
          <div>
            <label className="block text-sm text-slate-300 mb-2">
              Nom d'utilisateur
            </label>

            <input
              type="text"
              placeholder="Entrer username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-[#0f1117]
              border border-[#2d3748]
              rounded-xl px-4 py-3
              text-white outline-none
              focus:border-blue-500"
            />
          </div>

          {/* PASSWORD */}
          <div>
            <label className="block text-sm text-slate-300 mb-2">
              Mot de passe
            </label>

            <input
              type="password"
              placeholder="Entrer mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-[#0f1117]
              border border-[#2d3748]
              rounded-xl px-4 py-3
              text-white outline-none
              focus:border-blue-500"
            />
          </div>

          {/* BUTTON */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600
            hover:bg-blue-700
            transition-all duration-200
            py-3 rounded-xl
            text-white font-semibold"
          >
            {loading ? "Connexion..." : "Se connecter"}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-slate-400 text-sm">Vous n'avez pas de compte ?</p>

          <a
            href="/inscription"
            className="inline-block mt-3
            bg-[#1e293b]
            hover:bg-[#334155]
            border border-[#334155]
            text-blue-400
            px-5 py-2 rounded-xl
            transition-all duration-200"
          >
            Créer un compte étudiant
          </a>
        </div>

        {/* ========================================= */}
        {/* FOOTER */}
        {/* ========================================= */}
        <p className="text-center text-slate-500 text-sm mt-6">
          Plateforme universitaire E-Scolaire
        </p>
      </div>
    </div>
  );
}