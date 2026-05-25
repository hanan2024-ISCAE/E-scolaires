import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext'
import Toast from '../components/Toast'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [toast, setToast] = useState('')
  const { login } = useAuth()
  const nav = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    try {
      const u = await login(username, password)
      nav(u.role === 'admin' ? '/admin/notes' : '/notes')
    } catch {
      setToast('Identifiants incorrects')
    }
  }

  return (
    <div className="login-wrap login-page">
      <div className="login-box">
        <div className="login-logo">
          <div className="login-mark"><i className="ti ti-school" style={{ color: '#fff' }} /></div>
          <h2>Bon retour !</h2>
          <p>Connectez-vous à votre espace E-Scolaire</p>
        </div>
        <form className="login-card" onSubmit={submit}>
          <div className="form-group">
            <label className="form-label">Identifiant (matricule ou admin)</label>
            <input className="form-input" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="20230456" required />
          </div>
          <div className="form-group">
            <label className="form-label">Mot de passe</label>
            <input className="form-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button className="btn btn-primary" style={{ width: '100%', justifyContent: 'center' }} type="submit">
            <i className="ti ti-login" /> Se connecter
          </button>
        </form>
      </div>
      <Toast msg={toast} onClose={() => setToast('')} />
    </div>
  )
}
