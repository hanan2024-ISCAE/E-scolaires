import { useEffect, useState } from "react";

export default function AdminAttestations() {
  const [etudiants, setEtudiants] = useState([]);

  const [etudiantSelectionne, setEtudiantSelectionne] = useState("");

  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);

  // ==========================================
  // TOKEN
  // ==========================================
  const token = localStorage.getItem("access");

  // ==========================================
  // RECUPERER ETUDIANTS
  // ==========================================
  useEffect(() => {
    fetchEtudiants();
  }, []);

  async function fetchEtudiants() {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/etudiants/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      setEtudiants(data);

      if (data.length > 0) {
        setEtudiantSelectionne(data[0].matricule);
      }
    } catch (error) {
      console.log(error);
    }
  }

  // ==========================================
  // GENERER PDF
  // ==========================================
  async function handleGenerer() {
    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/api/generer_attestation/",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            matricule: etudiantSelectionne,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Erreur lors de la génération");
        setLoading(false);
        return;
      }

      setMessage(data.message);
    } catch (error) {
      console.log(error);

      setMessage("Erreur serveur");
    }

    setLoading(false);
  }

  function logout() {
    localStorage.clear();

    window.location.href = "/";
  }

  // ==========================================
  // ETUDIANT ACTUEL
  // ==========================================
  const etudiant = etudiants.find((e) => e.matricule === etudiantSelectionne);

  return (
    <div className="min-h-screen bg-[#0f1117] text-white flex">
      {/* ========================================== */}
      {/* SIDEBAR */}
      {/* ========================================== */}
      <div className="w-64 bg-[#161b27] border-r border-[#2d3748] p-5 sticky top-0 h-screen self-start">
        <h1 className="text-2xl font-bold mb-8 text-blue-400">E-Scolaire</h1>

        <div className="space-y-2">
          <button className="w-full text-left hover:bg-[#1f2937] px-4 py-3 rounded-lg">
            Étudiants
          </button>

          <button className="w-full text-left hover:bg-[#1f2937] px-4 py-3 rounded-lg">
            Notes
          </button>
          <button className="w-full text-left bg-[#1e3a5f] text-blue-400 px-4 py-3 rounded-lg">
            Attestations
          </button>
          <button
            onClick={logout}
            className="w-full text-left px-4 py-3 rounded-xl
            hover:bg-red-600 transition"
          >
            Déconnexion
          </button>
        </div>
      </div>

      {/* ========================================== */}
      {/* CONTENU */}
      {/* ========================================== */}
      <div className="flex-1 p-8 overflow-y-auto">
        {/* HEADER */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold">Génération des attestations</h1>

            <p className="text-slate-400 mt-1">
              Générer les attestations officielles des étudiants
            </p>
          </div>

          <div className="bg-[#1a2035] px-4 py-2 rounded-lg border border-[#2d3748]">
            Admin
          </div>
        </div>

        {/* GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* ========================================== */}
          {/* FORMULAIRE */}
          {/* ========================================== */}
          <div className="bg-[#1a2035] h-80 border border-[#2d3748] rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-6">
              Générer une attestation
            </h2>

            {/* SELECT ETUDIANT */}
            <div className="mb-5">
              <label className="block text-sm mb-2 text-slate-300">
                Étudiant
              </label>

              <select
                value={etudiantSelectionne}
                onChange={(e) => setEtudiantSelectionne(e.target.value)}
                className="w-full bg-[#0f1117] border border-[#2d3748]
                rounded-lg px-4 py-3 text-white outline-none"
              >
                {etudiants.map((e) => (
                  <option key={e.matricule} value={e.matricule}>
                    {e.first_name} {e.last_name} — {e.matricule}
                  </option>
                ))}
              </select>
            </div>

            {/* MESSAGE */}
            {message && (
              <div className="mb-4 bg-green-500/10 border border-green-500/30 text-green-400 px-4 py-3 rounded-lg">
                {message}
              </div>
            )}

            {/* BUTTON */}
            <button
              onClick={handleGenerer}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700
              py-3 rounded-xl font-semibold transition"
            >
              {loading ? "Génération..." : "Générer l'attestation"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
