import { useCallback, useEffect, useState } from 'react'
import { accepterReclamation, getReclamations, refuserReclamation } from '../api'
import Toast from '../components/Toast'

const badge = (s) => ({ en_attente: 'b-amber', acceptee: 'b-green', refusee: 'b-rose' }[s] || 'b-gray')
const label = (s) => ({ en_attente: 'En attente', acceptee: 'Acceptée', refusee: 'Refusée' }[s] || s)

export default function AdminReclamations() {
  const [rows, setRows] = useState([])
  const [toast, setToast] = useState('')
  const load = useCallback(() => getReclamations().then((r) => setRows(r.data)), [])

  useEffect(() => { load() }, [load])

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
        <div className="sprint-tag s2">Sprint 2</div>
        <h1>Traiter les Réclamations</h1>
        <p>Accepter ou refuser les contestations de notes</p>
      </div>
      <div className="table-wrap">
        <table>
          <thead><tr><th>Étudiant</th><th>Note</th><th>Module</th><th>Motif</th><th>Date</th><th>Statut</th><th>Actions</th></tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td><div className="student-row"><div className="s-av">{r.etudiant_nom?.split(' ').map((w) => w[0]).join('').slice(0, 2)}</div><div style={{ fontWeight: 600 }}>{r.etudiant_nom}</div></div></td>
                <td><span style={{ fontFamily: 'var(--mono)', color: 'var(--amber2)', fontWeight: 700 }}>{r.valeur_contestee}/20</span></td>
                <td>{r.module}</td>
                <td style={{ fontSize: 12, color: 'var(--text2)', maxWidth: 160 }}>{r.motif}</td>
                <td style={{ fontSize: 12, color: 'var(--text3)' }}>{new Date(r.created_at).toLocaleDateString('fr-FR')}</td>
                <td><span className={`badge ${badge(r.statut)}`}>{label(r.statut)}</span></td>
                <td>
                  {r.statut === 'en_attente' ? (
                    <div className="actions">
                      <button className="btn btn-success btn-sm" onClick={() => act(accepterReclamation, r.id, 'Réclamation acceptée !')}><i className="ti ti-check" />Accepter</button>
                      <button className="btn btn-danger btn-sm" onClick={() => act(refuserReclamation, r.id, 'Réclamation refusée.')}><i className="ti ti-x" />Refuser</button>
                    </div>
                  ) : r.nouvelle_valeur ? <span style={{ fontSize: 12, color: 'var(--text3)' }}>→ {r.nouvelle_valeur}/20</span> : null}
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
