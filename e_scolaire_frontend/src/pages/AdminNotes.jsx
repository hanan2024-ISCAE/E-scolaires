import { useCallback, useEffect, useState } from 'react'
import { getModules, getNotes, getStudents, publierNote } from '../api'
import Toast from '../components/Toast'

const emptyForm = {
  etudiant_id: '',
  module_id: '',
  type_note: 'examen',
  valeur: '',
  coefficient: '',
}

export default function AdminNotes() {
  const [rows, setRows] = useState([])
  const [students, setStudents] = useState([])
  const [modules, setModules] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [toast, setToast] = useState('')
  const [saving, setSaving] = useState(false)

  const load = useCallback(() => {
    getNotes().then((r) => setRows(r.data.data || r.data))
    getStudents().then((r) => setStudents(r.data)).catch((err) => {
      console.error('Error loading students:', err.response?.status, err.response?.data)
      setToast('Erreur lors du chargement des etudiants')
    })
    getModules().then((r) => {
      const modulesData = r.data.data || r.data
      setModules(modulesData)
    }).catch((err) => {
      console.error('Error loading modules:', err.response?.status, err.response?.data)
      setToast('Erreur lors du chargement des modules')
    })
  }, [])

  useEffect(() => { 
    load()
    // Poll for new students every 5 seconds
    const interval = setInterval(() => {
      getStudents().then((r) => setStudents(r.data))
    }, 5000)
    return () => clearInterval(interval)
  }, [load])

  const change = (e) => {
    if (e.target.name === 'module_id') {
      const selected = modules.find((m) => String(m.id) === e.target.value)
      setForm({ ...form, module_id: e.target.value, coefficient: selected?.coefficient ?? '' })
      return
    }
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const submit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await publierNote(form)
      setToast('Note publiee avec succes.')
      setForm(emptyForm)
      load()
    } catch (err) {
      const data = err.response?.data
      const errors = data?.errors || data
      const message =
        data?.error ||
        (errors?.etudiant_id?.[0]) ||
        (errors?.module_id?.[0]) ||
        (errors?.valeur?.[0]) ||
        (errors?.type_note?.[0]) ||
        (typeof errors === 'string' ? errors : null) ||
        'Erreur lors de la publication'
      setToast(message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <>
      <div className="ph">
        <div className="sprint-tag s2">Sprint 2</div>
        <h1>Publication des Notes</h1>
        <p>Publier les notes des etudiants et consulter l'historique</p>
      </div>

      <form className="table-wrap" onSubmit={submit} style={{ padding: 18, marginBottom: 16 }}>
        <div className="grid-2">
          <div>
            <label className="form-label">Etudiant</label>
            <select className="form-input" name="etudiant_id" value={form.etudiant_id} onChange={change} required>
              <option value="">Choisir un etudiant</option>
              {students.map((s) => {
                const name = `${s.first_name || ''} ${s.last_name || ''}`.trim() || s.username
                return <option key={s.id} value={s.id}>{name} - {s.matricule || s.username}</option>
              })}
            </select>
          </div>
          <div>
            <label className="form-label">Module</label>
            <select className="form-input" name="module_id" value={form.module_id} onChange={change} required>
              <option value="">Choisir un module</option>
              {modules.map((m) => (
                <option key={m.id} value={m.id}>{m.intitule} - {m.semestre}</option>
              ))}
            </select>
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
            <input className="form-input" value={form.coefficient || ''} disabled placeholder="Choisir un module" />
          </div>
          <div>
            <label className="form-label">Note / 20</label>
            <input className="form-input" type="number" min="0" max="20" step="0.25" name="valeur" value={form.valeur} onChange={change} required />
          </div>
        </div>
        {!students.length && (
          <p style={{ marginTop: 12, color: 'var(--text3)', fontSize: 12 }}>
            Aucun etudiant trouve dans la base de donnees actuelle.
          </p>
        )}
        {!modules.length && (
          <p style={{ marginTop: 12, color: 'var(--text3)', fontSize: 12 }}>
            Aucun module trouve dans la base de donnees actuelle.
          </p>
        )}
        <button className="btn btn-primary" disabled={saving || !students.length || !modules.length} style={{ marginTop: 14 }}>
          <i className="ti ti-send" />{saving ? 'Publication...' : 'Publier la note'}
        </button>
      </form>

      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>Etudiant</th><th>Matricule</th><th>Module</th><th>Type</th><th>Note</th><th>Coefficient</th><th>Date</th></tr>
          </thead>
          <tbody>
            {rows.map((n) => (
              <tr key={n.id}>
                <td>{n.etudiant?.full_name || n.etudiant?.username || '-'}</td>
                <td><span style={{ fontFamily: 'var(--mono)', color: 'var(--blue2)' }}>{n.etudiant?.matricule || '-'}</span></td>
                <td>{n.module?.intitule || n.module}</td>
                <td><span className="badge b-blue">{n.type_note}</span></td>
                <td style={{ fontWeight: 700 }}>{n.valeur}/20</td>
                <td>{n.module?.coefficient || n.coefficient}</td>
                <td style={{ fontSize: 12, color: 'var(--text3)' }}>{new Date(n.date_publication).toLocaleDateString('fr-FR')}</td>
              </tr>
            ))}
            {!rows.length && (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', color: 'var(--text3)', padding: 24 }}>
                  Aucune note publiee dans la base de donnees actuelle.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <Toast msg={toast} onClose={() => setToast('')} />
    </>
  )
}
