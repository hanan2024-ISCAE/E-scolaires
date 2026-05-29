import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import AdminAttestations from "./pages/AdminAttestations";
import InterfaceEtudiant from "./pages/InterfaceEtudiant";
import DemandeInscription from "./pages/DemandeInscription";

function App() {
  // =========================
  // TOKEN + ROLE
  // =========================
  const token = localStorage.getItem("access");

  const role = localStorage.getItem("role");

  // =========================
  // NON CONNECTE
  // =========================
  if (!token) {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />

          <Route path="/inscription" element={<DemandeInscription />} />

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    );
  }

  // =========================
  // CONNECTE
  // =========================
  return (
    <BrowserRouter>
      <Routes>
        {/* ADMIN */}
        {role === "admin" && (
          <>
            <Route path="/" element={<AdminAttestations />} />

            <Route path="*" element={<Navigate to="/" />} />
          </>
        )}

        {/* ETUDIANT */}
        {role === "etudiant" && (
          <>
            <Route path="/" element={<InterfaceEtudiant />} />

            <Route path="*" element={<Navigate to="/" />} />
          </>
        )}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
