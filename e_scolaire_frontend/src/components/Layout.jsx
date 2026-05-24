import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext'

export default function Layout({ admin }) {
  const { user, logout } = useAuth()
  const nav = useNavigate()
  const name = `${user?.first_name || ''} ${user?.last_name || ''}`.trim() || user?.username
  const initials = name.split(' ').map((w) => w[0]).join('').slice(0, 2).toUpperCase()

  const adminLinks = [
    ['/admin/inscriptions', 'ti-user-check', 'Inscriptions'],
    ['/admin/reclamations', 'ti-messages', 'Réclamations'],
  ]
  const studentLinks = [['/ressources', 'ti-folder-open', 'Ressources']]

  return (
    <>
      <div className="topbar">
        <div className="logo">
          <div className="logo-mark"><i className="ti ti-school" style={{ color: '#fff' }} /></div>
          <div className="logo-text">E-<span>Scolaire</span></div>
        </div>
        <div className="nav-right">
          <div className="avatar-pill">
            <div className="av-img"><span>{initials}</span></div>
            <span className="av-name">{name}</span>
          </div>
          <button className="btn btn-ghost btn-sm" onClick={() => { logout(); nav('/login') }}>
            <i className="ti ti-logout" /> Déconnexion
          </button>
        </div>
      </div>
      <div className="app">
        <div className="dash-layout">
          <div className="sidebar">
            <div className="sb-lbl">{admin ? 'Administration' : 'Étudiant'}</div>
            {(admin ? adminLinks : studentLinks).map(([to, icon, label]) => (
              <NavLink key={to} to={to} className={({ isActive }) => `sb-item${isActive ? ' active' : ''}`}>
                <i className={`ti ${icon}`} />{label}
              </NavLink>
            ))}
          </div>
          <div className="main-area"><Outlet /></div>
        </div>
      </div>
    </>
  )
}
