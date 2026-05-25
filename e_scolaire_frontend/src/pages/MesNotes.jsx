import { useCallback, useEffect, useState } from 'react'
import { getMesNotes } from '../api'

export default function MesNotes() {
  const [rows, setRows] = useState([])

  const load = useCallback(() => getMesNotes().then((r) => setRows(r.data)), [])

  useEffect(() => { load() }, [load])

  const moyenne = rows.length
    ? rows.reduce((sum, n) => sum + Number(n.valeur) * Number(n.coefficient), 0) / rows.reduce((sum, n) => sum + Number(n.coefficient), 0)
    : null

  return (
    <>
      <div className="ph">
        <div className="sprint-tag s2">Sprint 2</div>
        <h1>Mes Notes</h1>
        <p>Consultez les notes publiées par l'administration</p>
      </div>

      <div className="stats-grid" style={{ marginBottom: 16 }}>
        <div className="stat-card">
          <span>Notes publiées</span>
          <strong>{rows.length}</strong>
        </div>
        <div className="stat-card">
          <span>Moyenne pondérée</span>
          <strong>{moyenne === null ? '-' : moyenne.toFixed(2)}</strong>
        </div>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>Module</th><th>Type</th><th>Note</th><th>Coefficient</th><th>Date publication</th></tr>
          </thead>
          <tbody>
            {rows.map((n) => (
              <tr key={n.id}>
                <td>{n.module}</td>
                <td><span className="badge b-blue">{n.type_note}</span></td>
                <td style={{ fontWeight: 700, color: Number(n.valeur) >= 10 ? 'var(--green)' : 'var(--rose)' }}>{n.valeur}/20</td>
                <td>{n.coefficient}</td>
                <td style={{ fontSize: 12, color: 'var(--text3)' }}>{new Date(n.date_publication).toLocaleDateString('fr-FR')}</td>
              </tr>
            ))}
            {!rows.length && (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center', color: 'var(--text3)', padding: 24 }}>Aucune note publiée pour le moment.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  )
}
