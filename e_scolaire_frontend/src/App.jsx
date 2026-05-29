import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import AdminInscriptions from './pages/AdminInscriptions'
import AdminNotes from './pages/AdminNotes'
import AdminReclamations from './pages/AdminReclamations'
import MesNotes from './pages/MesNotes'
import Ressources from './pages/Ressources'

function Guard({ admin, children }) {
  const auth = useAuth()
  const user = auth?.user
  const loading = auth?.loading
  if (loading) return null
  if (!user) return <Navigate to="/login" replace />
  if (admin && user.role !== 'admin') return <Navigate to="/notes" replace />
  if (!admin && user.role === 'admin') return <Navigate to="/admin/notes" replace />
  return children
}

export default function App() {
  const auth = useAuth()
  const user = auth?.user
  const defaultPath = user?.role === 'admin' ? '/admin/notes' : '/notes'

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to={defaultPath} /> : <Login />} />
      <Route element={<Guard admin><Layout admin /></Guard>}>
        <Route path="/admin/inscriptions" element={<AdminInscriptions />} />
        <Route path="/admin/notes" element={<AdminNotes />} />
        <Route path="/admin/reclamations" element={<AdminReclamations />} />
      </Route>
      <Route element={<Guard admin={false}><Layout admin={false} /></Guard>}>
        <Route path="/notes" element={<MesNotes />} />
        <Route path="/ressources" element={<Ressources />} />
      </Route>
      <Route path="*" element={<Navigate to={user ? defaultPath : '/login'} replace />} />
    </Routes>
  )
}
