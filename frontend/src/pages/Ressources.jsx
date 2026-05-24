import { useCallback, useEffect, useState } from 'react'
import { downloadRessource, getRessources } from '../api'
import Toast from '../components/Toast'

const TYPES = ['', 'cours', 'td', 'tp', 'video']
const icons = { cours: 'ti ti-file-text txt-blue', td: 'ti ti-notes txt-green', tp: 'ti ti-code txt-amber', video: 'ti ti-video txt-cyan' }
const fmt = (n) => (n < 1024 ? `${n} o` : n < 1048576 ? `${(n / 1024).toFixed(0)} Ko` : `${(n / 1048576).toFixed(1)} Mo`)

export default function Ressources() {
  const [rows, setRows] = useState([])
  const [type, setType] = useState('')
  const [search, setSearch] = useState('')
  const [toast, setToast] = useState('')

  const load = useCallback(() => {
    const params = {}
    if (type) params.type = type
    if (search) params.search = search
    getRessources(params).then((r) => setRows(r.data))
  }, [type, search])

  useEffect(() => { load() }, [load])

  const dl = async (id, titre) => {
    try {
      const { data } = await downloadRessource(id)
      const url = URL.createObjectURL(data)
      const a = document.createElement('a')
      a.href = url
      a.download = titre.replace(/\s+/g, '_') + '.pdf'
      a.click()
      URL.revokeObjectURL(url)
      setToast('Téléchargement démarré...')
    } catch {
      setToast('Erreur de téléchargement')
    }
  }

  return (
    <>
      <div className="ph">
        <div className="sprint-tag s3">Sprint 3</div>
        <h1>Ressources Pédagogiques</h1>
        <p>Téléchargez les cours, TD, TP publiés par vos enseignants</p>
      </div>
      <div className="filter-row">
        {['Tous', 'Cours', 'TD', 'TP', 'Vidéo'].map((l, i) => (
          <button key={l} className={`filter-btn${type === TYPES[i] ? ' on' : ''}`} onClick={() => setType(TYPES[i])}>{l}</button>
        ))}
        <input className="form-input filter-search" placeholder="Rechercher..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {rows.map((r) => (
          <div className="res-card" key={r.id}>
            <div className="res-icon" style={{ background: 'rgba(59,130,246,.12)' }}>
              <i className={icons[r.type_ressource] || 'ti ti-file txt-blue'} style={{ fontSize: 17 }} />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 13.5, fontWeight: 600 }}>{r.titre}</div>
              <div style={{ fontSize: 11.5, color: 'var(--text2)' }}>{r.module} · {r.niveau} · {r.annee_scolaire} · {fmt(r.taille)}</div>
            </div>
            <button className="btn btn-ghost btn-sm" onClick={() => dl(r.id, r.titre)}><i className="ti ti-download" />Télécharger</button>
          </div>
        ))}
      </div>
      <Toast msg={toast} onClose={() => setToast('')} />
    </>
  )
}
