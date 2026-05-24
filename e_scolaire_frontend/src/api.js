import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((cfg) => {
  const t = localStorage.getItem('token')
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})

export const login = (username, password) => api.post('/auth/login/', { username, password })
export const me = () => api.get('/auth/me/')

export const getDemandes = (statut) => api.get('/inscriptions/demandes/', { params: statut ? { statut } : {} })
export const validerDemande = (id) => api.post(`/inscriptions/demandes/${id}/valider/`)
export const refuserDemande = (id, motif_refus = '') => api.post(`/inscriptions/demandes/${id}/refuser/`, { motif_refus })

export const getReclamations = (statut) => api.get('/reclamations/', { params: statut ? { statut } : {} })
export const accepterReclamation = (id, body = {}) => api.post(`/reclamations/${id}/accepter/`, body)
export const refuserReclamation = (id, body = {}) => api.post(`/reclamations/${id}/refuser/`, body)

export const getRessources = (params) => api.get('/ressources/', { params })
export const downloadRessource = (id) => api.get(`/ressources/${id}/telecharger/`, { responseType: 'blob' })

export default api
