import { useCallback, useEffect, useState } from 'react'
import { getNotes, publierNote } from '../api'
import Toast from '../components/Toast'

const emptyForm = {
  etudiant: '',
  module: '',
  type_note: 'examen',
  valeur: '',
  coefficient: 4,
}

export default function AdminNotes() {
  const [rows, setRows] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [toast, setToast] = useState('')
  const [saving, setSaving] = useState(false)

  const load = useCallback(() => getNotes().then((r) => setRows(r.data)), [])

  useEffect(() => { load() }, [load])

  const change = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await publierNote(form)
      setToast('Note publiée avec succès.')
      setForm(emptyForm)
      load()
    } catch (err) {
      const data = err.response?.data
      setToast(data?.detail || data?.etudiant?.[0] || data?.valeur?.[0] || 'Erreur lors de la publication')
    } finally {
      setSaving(false)
    }
  }

  return (
    <>
      <div className="ph">
        <div className="sprint-tag s2">Sprint 2</div>
        <h1>Publication des Notes</h1>
        <p>Publier les notes des étudiants et consulter l'historique</p>
      </div>

      <form className="table-wrap" onSubmit={submit} style={{ padding: 18, marginBottom: 16 }}>
        <div className="grid-2">
          <div>
            <label className="form-label">Matricule ou username étudiant</label>
            <input className="form-input" name="etudiant" value={form.etudiant} onChange={change} placeholder="ex: 28238456" required />
          </div>
          <div>
            <label className="form-label">Module</label>
            <input className="form-input" name="module" value={form.module} onChange={change} placeholder="Programmation web" required />
          </div>
          <div>
            <label className="form-label">Type</label>
            <select className="form-input" name="type_note" value={form.type_note} onChange={change}>
              <option value="ds">DS</option>
              <option value="tp">TP</option>
              <option value="examen">Examen</option>
              <option value="rattrapage">Rattrapage</option>
            </select>
          </div>
          <div>
            <label className="form-label">Coefficient</label>
            <input className="form-input" type="number" min="1" name="coefficient" value={form.coefficient} onChange={change} required />
          </div>
          <div>
            <label className="form-label">Note / 20</label>
            <input className="form-input" type="number" min="0" max="20" step="0.25" name="valeur" value={form.valeur} onChange={change} required />
          </div>
        </div>
        <button className="btn btn-primary" disabled={saving} style={{ marginTop: 14 }}>
          <i className="ti ti-send" />{saving ? 'Publication...' : 'Publier la note'}
        </button>
      </form>

      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>Étudiant</th><th>Matricule</th><th>Module</th><th>Type</th><th>Note</th><th>Coefficient</th><th>Date</th></tr>
          </thead>
          <tbody>
            {rows.map((n) => (
              <tr key={n.id}>
                <td>{n.etudiant_nom}</td>
                <td><span style={{ fontFamily: 'var(--mono)', color: 'var(--blue2)' }}>{n.etudiant_matricule || '-'}</span></td>
                <td>{n.module}</td>
                <td><span className="badge b-blue">{n.type_note}</span></td>
                <td style={{ fontWeight: 700 }}>{n.valeur}/20</td>
                <td>{n.coefficient}</td>
                <td style={{ fontSize: 12, color: 'var(--text3)' }}>{new Date(n.date_publication).toLocaleDateString('fr-FR')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Toast msg={toast} onClose={() => setToast('')} />
    </>
  )
}
