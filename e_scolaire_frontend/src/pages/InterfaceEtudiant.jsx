import { useEffect, useRef, useState } from "react";

import html2canvas from "html2canvas";

import jsPDF from "jspdf";

export default function InterfaceEtudiant() {
  // =========================================
  // STATES
  // =========================================
  const [data, setData] = useState(null);

  const [loading, setLoading] = useState(false);

  // =========================================
  // LOCAL STORAGE
  // =========================================
  const token = localStorage.getItem("access");

  const username = localStorage.getItem("username");

  // =========================================
  // REF PDF
  // =========================================
  const pdfRef = useRef();

  // =========================================
  // FETCH DATA
  // =========================================
  useEffect(() => {
    fetchAttestation();
  }, []);

  async function fetchAttestation() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/details-attestation",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      const result = await response.json();

      console.log(result);

      setData(result);
    } catch (error) {
      console.log(error);
    }
  }

  // =========================================
  // TELECHARGER PDF
  // =========================================
  async function telechargerPDF() {
    try {
      setLoading(true);

      const element = pdfRef.current;

      // =====================================
      // AFFICHER TEMPORAIREMENT
      // =====================================
 

      // =====================================
      // CAPTURE
      // =====================================
      const canvas = await html2canvas(element, {
        scale: 2,
      });

      const imgData = canvas.toDataURL("image/png");

      // =====================================
      // PDF
      // =====================================
      const pdf = new jsPDF("p", "mm", "a4");

      const width = 210;

      const height = (canvas.height * width) / canvas.width;

      pdf.addImage(imgData, "PNG", 0, 0, width, height);

      // =====================================
      // TELECHARGEMENT
      // =====================================
      pdf.save("attestation.pdf");

      // =====================================
      // RECACHER
      // =====================================
      element.style.display = "none";
    } catch (error) {
      console.log(error);
    }

    setLoading(false);
  }

  // =========================================
  // LOGOUT
  // =========================================
  function logout() {
    localStorage.clear();

    window.location.href = "/";
  }

  return (
    <div className="min-h-screen bg-[#0b1120] text-white flex">
      {/* ========================================= */}
      {/* SIDEBAR */}
      {/* ========================================= */}
      <div className="w-72 bg-[#111827] border-r border-[#1f2937] p-6">
        <div className="flex items-center gap-3 mb-10">
          <div
            className="w-12 h-12 rounded-xl
            bg-gradient-to-br from-blue-500 to-indigo-600"
          />

          <div>
            <h1 className="text-2xl font-bold">E-Scolaire</h1>

            <p className="text-slate-400 text-sm">Portail étudiant</p>
          </div>
        </div>

        {/* MENU */}
        <div
          className="
    fixed
    h-screen
    w-64
    text-white
    overflow-y-auto
  "
        >
          {/* ETUDIANT */}
          <div>
            <p className="text-xs text-slate-500 uppercase mb-2">Étudiant</p>

            <button
              className="w-full text-left px-4 py-3 rounded-xl
      hover:bg-slate-800 transition"
            >
              Tableau de bord
            </button>

            <button
              className="w-full text-left px-4 py-3 rounded-xl
      hover:bg-slate-800 transition"
            >
              Mon profil
            </button>
          </div>

          {/* ACADEMIQUE */}
          <div className="pt-4 border-t border-slate-800">
            <p className="text-xs text-slate-500 uppercase mb-2">Académique</p>

            <button
              className="w-full text-left px-4 py-3 rounded-xl
      hover:bg-slate-800 transition"
            >
              Mes notes
            </button>

            <button
              className="w-full text-left px-4 py-3 rounded-xl
      hover:bg-slate-800 transition"
            >
              Réclamations
            </button>

            <button
              className="w-full text-left px-4 py-3 rounded-xl
      hover:bg-slate-800 transition"
            >
              Ressources
            </button>
          </div>

          {/* SERVICES */}
          <div className="pt-4 border-t border-slate-800">
            <p className="text-xs text-slate-500 uppercase mb-2">Services</p>

            <button
              className="w-full text-left px-4 py-3 rounded-xl
      hover:bg-slate-800 transition"
            >
              Logement
            </button>

            <button
              className="w-full text-left px-4 py-3 rounded-xl
      bg-blue-600 text-white"
            >
              Attestations
            </button>
          </div>

          {/* DECONNEXION */}
          <div className="pt-4 border-t border-slate-800">
            <button
              onClick={logout}
              className="w-full text-left px-4 py-3 rounded-xl
      hover:bg-red-600 transition"
            >
              Déconnexion
            </button>
          </div>
        </div>
      </div>

      {/* ========================================= */}
      {/* CONTENT */}
      {/* ========================================= */}
      <div className="flex-1 overflow-y-auto">
        {/* HEADER */}
        <div
          className="bg-[#111827]
          border-b border-[#1f2937]
          px-8 py-5 flex items-center justify-between"
        >
          <div>
            <h1 className="text-3xl font-bold">Attestation d'inscription</h1>

            <p className="text-slate-400 mt-1">
              Téléchargez votre attestation officielle
            </p>
          </div>

          {/* USER */}
          <div
            className="flex items-center gap-3
            bg-[#1e293b] px-4 py-2 rounded-xl"
          >
            <div
              className="w-10 h-10 rounded-full
              bg-blue-600 flex items-center justify-center
              font-bold"
            >
              {username?.slice(0, 2).toUpperCase()}
            </div>

            <div>
              <p className="font-semibold">{username}</p>

              <p className="text-xs text-slate-400">Étudiant</p>
            </div>
          </div>
        </div>

        {/* BODY */}
        <div className="p-8">
          {!data ? (
            <div
              className="bg-[#111827]
              border border-[#1f2937]
              rounded-2xl p-10 text-center"
            >
              Chargement...
            </div>
          ) : (
            <>
              {/* ========================================= */}
              {/* PDF ZONE */}
              {/* ========================================= */}
              <div
                ref={pdfRef}
                id="attestation"
                className="bg-white text-black
w-[900px] p-12"
                style={{
                  position: "absolute",
                  left: "-9999px",
                  top: 0,
                }}
              >
                <div className="mb-10 text-black">
                  {/* PREMIERE LIGNE */}
                  <div className="flex justify-between items-center">
                    <h2 className="text-xl text-black uppercase">
                      République Islamique de Mauritanie
                    </h2>

                    <p className="text-lg font-semibold">
                      Honneur - Fraternité - Justice
                    </p>
                  </div>

                  {/* DEUXIEME LIGNE */}
                  <p className="text-lg font-semibold">
                    Ministère de l’Enseignement Supérieur
                  </p>
                </div>

                {/* TITLE */}
                <div className="text-center mb-10">
                  <h2
                    className="text-3xl font-bold
                    uppercase text-blue-700"
                  >
                    Attestation d'inscription
                  </h2>
                </div>

                {/* TEXT */}
                <div className="leading-9 text-[17px]">
                  <p>
                    Le chef du service de la scolarité atteste par la présente
                    que :
                  </p>

                  <p className="mt-4">
                    L’étudiant(e) susmentionné(e) est régulièrement inscrit(e)
                    au sein de l’établissement pour l’année universitaire en
                    cours et poursuit normalement sa formation académique.
                  </p>

                  <p className="mt-4">
                    M(Mlle): <span className="font-bold">{username}</span>
                  </p>

                  <p className="mt-4">
                    matricule :
                    <span className="font-bold ml-2">
                      {data.etudiant.matricule}
                    </span>
                  </p>

                  <p className="mt-4">
                    En :
                    <span className="font-bold ml-2">
                      {data.etudiant.niveau}
                    </span>
                    <span className="font-bold ml-2">
                      {data.etudiant.filiere}:
                    </span>
                  </p>
                </div>

                {/* ========================================= */}
                {/* SEMESTRE 1 */}
                {/* ========================================= */}
                <div className="mt-10">
                  <h3
                    className="text-2xl font-bold
                    mb-5 text-blue-700"
                  >
                    Semestre 1
                  </h3>

                  <table className="w-full border border-black">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="border border-black p-3">Module</th>

                        <th className="border border-black p-3">Coefficient</th>
                      </tr>
                    </thead>

                    <tbody>
                      {data.modules_s1.map((module, index) => (
                        <tr key={index}>
                          <td className="border border-black p-3">
                            {module.intitule}
                          </td>

                          <td className="border border-black p-3 text-center">
                            {module.coefficient}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* ========================================= */}
                {/* SEMESTRE 2 */}
                {/* ========================================= */}
                <div className="mt-10">
                  <h3
                    className="text-2xl font-bold
                    mb-5 text-blue-700"
                  >
                    Semestre 2
                  </h3>

                  <table className="w-full border border-black">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="border border-black p-3">Module</th>

                        <th className="border border-black p-3">Coefficient</th>
                      </tr>
                    </thead>

                    <tbody>
                      {data.modules_s2.map((module, index) => (
                        <tr key={index}>
                          <td className="border border-black p-3">
                            {module.intitule}
                          </td>

                          <td className="border border-black p-3 text-center">
                            {module.coefficient}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* FOOTER */}
                <div className="mt-16 text-[17px]">
                  <p>
                    Cette attestation est délivrée pour servir et valoir ce que
                    de droit.
                  </p>

                  <div className="mt-20 text-right">
                    <p className="font-bold">Signature de l'administration</p>
                  </div>
                </div>
              </div>

              {/* BUTTON */}
              {/* ========================================= */}
              {/* CARD ATTESTATION */}
              {/* ========================================= */}
              <div
                className="bg-[#111827]
                border border-[#1f2937]
                rounded-2xl p-6 max-w-3xl ml-2"
              >
                {/* HEADER CARD */}
                <div className="flex justify-between items-start mb-6">
                  <span
                    className="bg-blue-500/20
                    text-blue-400
                    px-3 py-1 rounded-full text-sm"
                  >
                    inscription
                  </span>

                  <span className="text-slate-500 text-sm">
                    {new Date().toLocaleDateString()}
                  </span>
                </div>

                {/* TITRE */}
                <h2 className="text-2xl font-semibold mb-4">
                  Attestation officielle
                </h2>

                {/* DESCRIPTION */}
                <p className="text-slate-400 leading-8 mb-8">
                  Cette attestation officielle est disponible pour
                  téléchargement au format PDF. Elle contient les informations
                  académiques, les modules des semestres ainsi que les
                  informations administratives de l'étudiant.
                </p>

                {/* FOOTER */}
                <div className="flex justify-between items-center">
                  <span
                    className="bg-green-500/20
                    text-green-400
                    text-sm px-3 py-1 rounded-full"
                  >
                    Générée
                  </span>

                  <button
                    onClick={telechargerPDF}
                    disabled={loading}
                    className="bg-blue-600
                      hover:bg-blue-700
                      transition px-6 py-3 rounded-xl
                      font-semibold"
                  >
                    {loading ? "Téléchargement..." : "Télécharger PDF"}
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
