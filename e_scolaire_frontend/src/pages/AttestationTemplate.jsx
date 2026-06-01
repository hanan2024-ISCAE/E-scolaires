import React from "react";

export default function AttestationTemplate({
  etudiant,
  modulesS1,
  modulesS2,
}) {
  return (
    <div className="bg-gray-100 min-h-screen p-10">
      {/* PAGE */}
      <div
        className="bg-white max-w-5xl mx-auto
        p-14 shadow-2xl border border-gray-300"
      >
        {/* ===================================== */}
        {/* ENTETE */}
        {/* ===================================== */}
        <div className="flex justify-between items-start mb-12">
          {/* GAUCHE */}
          <div className="text-sm text-gray-700 leading-7">
            <p className="font-semibold">Honneur - Fraternité - Justice</p>
          </div>

          {/* CENTRE */}
          <div className="text-center">
            <div
              className="w-20 h-20 rounded-full
              bg-green-700 mx-auto mb-3"
            />

            <h1 className="text-2xl font-bold text-gray-800">UNIVERSITÉ</h1>

            <p className="text-gray-500">Plateforme E-Scolaire</p>
          </div>

          {/* DROITE */}
          <div className="text-right text-sm text-gray-700 leading-7">
            <p className="font-semibold">République Islamique de Mauritanie</p>

            <p>Ministère de l’Enseignement Supérieur</p>
          </div>
        </div>

        {/* ===================================== */}
        {/* TITRE */}
        {/* ===================================== */}
        <div className="text-center mb-14">
          <h1
            className="text-4xl font-extrabold
            text-blue-700 uppercase tracking-widest"
          >
            Attestation d'inscription
          </h1>

          <div
            className="w-40 h-1 bg-blue-600
            mx-auto mt-4 rounded-full"
          />
        </div>

        {/* ===================================== */}
        {/* INFORMATIONS */}
        {/* ===================================== */}
        <div className="space-y-6 text-gray-800 text-lg leading-9">
          <p>Je soussigné certifie que l'étudiant :</p>

          <div
            className="bg-blue-50 border-l-4 border-blue-600
            p-5 rounded-lg"
          >
            <p>
              <span className="font-semibold">Nom :</span> {etudiant.nom}
            </p>

            <p>
              <span className="font-semibold">Prénom :</span> {etudiant.prenom}
            </p>

            <p>
              <span className="font-semibold">Matricule :</span>{" "}
              {etudiant.matricule}
            </p>

            <p>
              <span className="font-semibold">Filière :</span>{" "}
              {etudiant.filiere}
            </p>

            <p>
              <span className="font-semibold">Niveau :</span> {etudiant.niveau}
            </p>
          </div>

          <p>Est régulièrement inscrit pour l’année universitaire en cours.</p>
        </div>

        {/* ===================================== */}
        {/* SEMESTRE 1 */}
        {/* ===================================== */}
        <div className="mt-14">
          <h2
            className="text-2xl font-bold text-blue-700
            mb-5"
          >
            Semestre 1
          </h2>

          <table
            className="w-full border-collapse
            overflow-hidden rounded-xl"
          >
            <thead>
              <tr className="bg-blue-600 text-white">
                <th className="p-4 text-left">Module</th>

                <th className="p-4 text-center">Coefficient</th>
              </tr>
            </thead>

            <tbody>
              {modulesS1.map((module, index) => (
                <tr
                  key={index}
                  className="border-b border-gray-200
                  hover:bg-blue-50"
                >
                  <td className="p-4">{module.intitule}</td>

                  <td className="p-4 text-center">{module.coefficient}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* ===================================== */}
        {/* SEMESTRE 2 */}
        {/* ===================================== */}
        <div className="mt-14">
          <h2
            className="text-2xl font-bold text-green-700
            mb-5"
          >
            Semestre 2
          </h2>

          <table
            className="w-full border-collapse
            overflow-hidden rounded-xl"
          >
            <thead>
              <tr className="bg-green-600 text-white">
                <th className="p-4 text-left">Module</th>

                <th className="p-4 text-center">Coefficient</th>
              </tr>
            </thead>

            <tbody>
              {modulesS2.map((module, index) => (
                <tr
                  key={index}
                  className="border-b border-gray-200
                  hover:bg-green-50"
                >
                  <td className="p-4">{module.intitule}</td>

                  <td className="p-4 text-center">{module.coefficient}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* ===================================== */}
        {/* SIGNATURE */}
        {/* ===================================== */}
        <div className="mt-20 flex justify-between items-end">
          <div>
            <p className="text-gray-500">Fait à Nouakchott</p>

            <p className="text-gray-500">
              Le : {new Date().toLocaleDateString()}
            </p>
          </div>

          <div className="text-center">
            <div
              className="w-40 h-40 border-4 border-blue-700
              rounded-full opacity-20 mb-4"
            />

            <p className="font-semibold text-gray-700">Signature & Cachet</p>
          </div>
        </div>
      </div>
    </div>
  );
}
