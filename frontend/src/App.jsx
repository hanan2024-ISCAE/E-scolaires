import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import AdminInscriptions from './pages/AdminInscriptions'
import AdminReclamations from './pages/AdminReclamations'
import Ressources from './pages/Ressources'

function Guard({ admin, children }) {
  const { user, loading } = useAuth()
  if (loading) return null
  if (!user) return <Navigate to="/login" replace />
  if (admin && user.role !== 'admin') return <Navigate to="/ressources" replace />
  if (!admin && user.role === 'admin') return <Navigate to="/admin/inscriptions" replace />
  return children
}

export default function App() {
  const { user } = useAuth()
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to={user.role === 'admin' ? '/admin/inscriptions' : '/ressources'} /> : <Login />} />
      <Route element={<Guard admin><Layout admin /></Guard>}>
        <Route path="/admin/inscriptions" element={<AdminInscriptions />} />
        <Route path="/admin/reclamations" element={<AdminReclamations />} />
      </Route>
      <Route element={<Guard admin={false}><Layout admin={false} /></Guard>}>
        <Route path="/ressources" element={<Ressources />} />
      </Route>
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}
