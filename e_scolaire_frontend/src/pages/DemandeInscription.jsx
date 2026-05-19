import { useState, useRef } from "react"
import axios from "axios"

export default function DemandeInscription() {
  const [form, setForm] = useState({
    prenom: "", nom: "", email: "", password: "",
    matricule: "", filiere: "Informatique", niveau: "L1", photo: null
  })
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const fileRef = useRef()

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleFile = (e) => {
    const file = e.target.files[0]
    if (!file) return
    setForm({ ...form, photo: file })
    const reader = new FileReader()
    reader.onload = ev => setPreview(ev.target.result)
    reader.readAsDataURL(file)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const data = new FormData()
    data.append("username", form.prenom + form.nom)
    data.append("email", form.email)
    data.append("password", form.password)
    data.append("matricule", form.matricule)
    data.append("filiere", form.filiere)
    data.append("niveau", form.niveau)
    if (form.photo) data.append("photo", form.photo)

    console.log("=== DONNÉES ENVOYÉES ===")
    for (let pair of data.entries()) console.log(pair[0], pair[1])

    setLoading(true)
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/register/", data)
      alert(res.data?.message || "Succès inscription")
    } catch (err) {
      console.log(err.response?.data)
      alert(JSON.stringify(err.response?.data))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#080d18] text-white w-full flex justify-center p-10">
        
      <div className="w-full max-w-[660px]">

        
        <h1 className=" text-white font-extrabold tracking-tight mb-1">
          Demande d'inscription
        </h1>
        <p className="text-white text-sm mb-7">
          Remplissez le formulaire — l'admin validera votre demande sous 48h
        </p>

        <form onSubmit={handleSubmit} className="space-y-3.5">

          {/* Photo */}
          <div className="bg-[#0d1525] border border-[rgba(99,140,255,0.13)] rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-[11px] font-bold tracking-[.1em] uppercase text-white">Photo de profil</span>
              <span className="text-[10px] font-semibold bg-[rgba(61,232,160,0.1)] text-[#3de8a0]
                border border-[rgba(61,232,160,0.22)] px-2 py-0.5 rounded-full">nouveau attribut</span>
            </div>
            <div className="flex items-center gap-3.5 bg-[#111d32] border border-[rgba(99,140,255,0.13)]
              rounded-xl p-4 hover:border-[rgba(99,140,255,0.32)] transition-colors">
              <div className="w-[54px] h-[54px] rounded-full bg-gradient-to-br from-[#2a4aaa] to-[#4f7cff]
                flex items-center justify-center overflow-hidden flex-shrink-0
                shadow-[0_0_0_3px_rgba(79,124,255,0.2)]">
                {preview
                  ? <img src={preview} className="w-full h-full object-cover" alt="preview"/>
                  : <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5">
                      <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
                    </svg>
                }
              </div>
              <div className="flex-1">
                <p className="font-bold text-[13px] mb-0.5">Photo officielle de l'étudiant</p>
                <p className="text-[11px] text-[#5a6a8a]">JPG, PNG · Max 5 Mo · 300×300px recommandé</p>
              </div>
              <button type="button"
                onClick={() => fileRef.current.click()}
                className="flex-shrink-0 text-xs text-[#8a9bb8] border border-[rgba(99,124,255,0.32)]
                  px-3 py-1.5 rounded-lg hover:bg-[rgba(79,124,255,0.08)] hover:text-[#7c9dff]
                  hover:border-[#4f7cff] transition-all">
                Choisir une photo
              </button>
              <input type="file" ref={fileRef} accept="image/*" onChange={handleFile} className="hidden"/>
            </div>
          </div>

          {/* Infos personnelles */}
          <div className="bg-[#0d1525] border border-[rgba(99,140,255,0.13)] rounded-2xl p-6">
            <p className="text-[10px] font-bold tracking-[.12em] uppercase text-[#5a6a8a]
              pb-3.5 border-b border-[rgba(99,140,255,0.13)] mb-5">Informations personnelles</p>

            <div className="grid grid-cols-2 gap-3 mb-3">
              {[["prenom","Prénom","Ahmed"],["nom","Nom","Benali"]].map(([name,label,ph]) => (
                <div key={name} className="flex flex-col gap-1.5">
                  <label className="text-[12px] font-medium text-[#8a9bb8]">{label}</label>
                  <input name={name} placeholder={ph} value={form[name]} onChange={handleChange}
                    className="bg-[#111d32] border border-[rgba(99,140,255,0.13)] rounded-[10px]
                      px-3.5 py-[11px] text-sm text-white placeholder-[#5a6a8a] outline-none
                      focus:border-[#4f7cff] focus:shadow-[0_0_0_3px_rgba(79,124,255,0.13)]
                      focus:bg-[#131f38] transition-all"/>
                </div>
              ))}
            </div>

            {[["email","Email","email","ahmed.benali@mail.com"],
              ["password","Mot de passe","password","Min. 8 caractères"]].map(([name,label,type,ph]) => (
              <div key={name} className="flex flex-col gap-1.5 mb-3 last:mb-0">
                <label className="text-[12px] font-medium text-[#8a9bb8]">{label}</label>
                <input name={name} type={type} placeholder={ph} value={form[name]} onChange={handleChange}
                  className="bg-[#111d32] border border-[rgba(99,140,255,0.13)] rounded-[10px]
                    px-3.5 py-[11px] text-sm text-white placeholder-[#5a6a8a] outline-none
                    focus:border-[#4f7cff] focus:shadow-[0_0_0_3px_rgba(79,124,255,0.13)]
                    focus:bg-[#131f38] transition-all"/>
              </div>
            ))}
          </div>

          {/* Infos académiques */}
          <div className="bg-[#0d1525] border border-[rgba(99,140,255,0.13)] rounded-2xl p-6">
            <p className="text-[10px] font-bold tracking-[.12em] uppercase text-[#5a6a8a]
              pb-3.5 border-b border-[rgba(99,140,255,0.13)] mb-5">Informations académiques</p>

            <div className="grid grid-cols-2 gap-3 mb-3">
              <div className="flex flex-col gap-1.5">
                <label className="text-[12px] font-medium text-[#8a9bb8]">Matricule</label>
                <input name="matricule" placeholder="28238456" value={form.matricule} onChange={handleChange}
                  className="bg-[#111d32] border border-[rgba(99,140,255,0.13)] rounded-[10px]
                    px-3.5 py-[11px] text-sm text-white placeholder-[#5a6a8a] outline-none
                    focus:border-[#4f7cff] focus:shadow-[0_0_0_3px_rgba(79,124,255,0.13)]
                    focus:bg-[#131f38] transition-all"/>
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-[12px] font-medium text-[#8a9bb8]">Filière</label>
                <select name="filiere" value={form.filiere} onChange={handleChange}
                  className="bg-[#111d32] border border-[rgba(99,140,255,0.13)] rounded-[10px]
                    px-3.5 py-[11px] text-sm text-white outline-none appearance-none
                    focus:border-[#4f7cff] focus:shadow-[0_0_0_3px_rgba(79,124,255,0.13)]
                    focus:bg-[#131f38] transition-all cursor-pointer">
                  <option value="Informatique">Informatique</option>
                  <option value="Mathématiques">Mathématiques</option>
                  <option value="Gestion">Gestion</option>
                </select>
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-[12px] font-medium text-[#8a9bb8]">Niveau</label>
              <select name="niveau" value={form.niveau} onChange={handleChange}
                className="bg-[#111d32] border border-[rgba(99,140,255,0.13)] rounded-[10px]
                  px-3.5 py-[11px] text-sm text-white outline-none appearance-none
                  focus:border-[#4f7cff] focus:shadow-[0_0_0_3px_rgba(79,124,255,0.13)]
                  focus:bg-[#131f38] transition-all cursor-pointer">
                <option value="L1">L1 — 1ère année Licence</option>
                <option value="L2">L2 — 2ème année Licence</option>
                <option value="L3">L3 — 3ème année Licence</option>
                <option value="M1">M1 — 1ère année Master</option>
              </select>
            </div>
          </div>

          <button type="submit" disabled={loading}
            className="w-full py-[14px] bg-gradient-to-r from-[#4f7cff] to-[#6a8fff]
              rounded-xl text-white font-bold text-[15px] tracking-wide
              shadow-[0_4px_22px_rgba(79,124,255,0.32)]
              hover:shadow-[0_7px_28px_rgba(79,124,255,0.45)] hover:-translate-y-px
              active:translate-y-0 disabled:opacity-60 disabled:cursor-not-allowed
              transition-all duration-200">
            {loading ? "Envoi en cours…" : "Envoyer la demande d'inscription"}
          </button>

        </form>
      </div>
    </div>
  )
}