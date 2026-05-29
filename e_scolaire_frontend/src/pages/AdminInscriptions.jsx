import { useCallback, useEffect, useState } from 'react'
import { getDemandes, refuserDemande, validerDemande } from '../api'
import Toast from '../components/Toast'

const badge = (s) => ({ en_attente: 'b-amber', validee: 'b-green', refusee: 'b-rose' }[s] || 'b-gray')
const label = (s) => ({ en_attente: 'En attente', validee: 'Validée', refusee: 'Refusée' }[s] || s)

export default function AdminInscriptions() {
  const [rows, setRows] = useState([])
  const [toast, setToast] = useState('')
  const load = useCallback(() => getDemandes().then((r) => setRows(r.data)), [])

  useEffect(() => { 
    load()
    // Poll for new inscriptions every 5 seconds
    const interval = setInterval(() => {
      getDemandes().then((r) => setRows(r.data))
    }, 5000)
    return () => clearInterval(interval)
  }, [load])

  const act = async (fn, id, ok) => {
    try {
      await fn(id)
      setToast(ok)
      load()
    } catch (e) {
      setToast(e.response?.data?.detail || 'Erreur')
    }
  }

  return (
    <>
      <div className="ph">
        <div className="sprint-tag s1">Sprint 1</div>
        <h1>Gestion des Inscriptions</h1>
        <p>Valider ou refuser les demandes d'inscription</p>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>Étudiant</th><th>Matricule</th><th>Filière</th><th>Niveau</th><th>Date</th><th>Statut</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {rows.map((d) => (
              <tr key={d.id}>
                <td>
                  <div className="student-row">
                    <div className="s-av">{d.prenom[0]}{d.nom[0]}</div>
                    <div><div style={{ fontWeight: 600 }}>{d.etudiant_nom}</div><div style={{ fontSize: 11, color: 'var(--text3)' }}>{d.email}</div></div>
                  </div>
                </td>
                <td><span style={{ fontFamily: 'var(--mono)', color: 'var(--blue2)' }}>{d.matricule}</span></td>
                <td>{d.filiere}</td>
                <td><span className="badge b-blue">{d.niveau}</span></td>
                <td style={{ fontSize: 12, color: 'var(--text3)' }}>{new Date(d.created_at).toLocaleDateString('fr-FR')}</td>
                <td><span className={`badge ${badge(d.statut)}`}>{label(d.statut)}</span></td>
                <td>
                  {d.statut === 'en_attente' ? (
                    <div className="actions">
                      <button className="btn btn-success btn-sm" onClick={() => act(validerDemande, d.id, 'Inscription validée !')}><i className="ti ti-check" />Valider</button>
                      <button className="btn btn-danger btn-sm" onClick={() => act((id) => refuserDemande(id, 'Dossier incomplet'), d.id, 'Inscription refusée.')}><i className="ti ti-x" />Refuser</button>
                    </div>
                  ) : <span className={`badge ${badge(d.statut)}`}>{label(d.statut)}</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Toast msg={toast} onClose={() => setToast('')} />
    </>
  )
}
