import { createContext, useContext, useEffect, useState } from 'react'
import { login as apiLogin, me } from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) return setLoading(false)
    me().then((r) => setUser(r.data)).catch(() => localStorage.removeItem('token')).finally(() => setLoading(false))
  }, [])

  const login = async (username, password) => {
    const { data } = await apiLogin(username, password)
    localStorage.setItem('token', data.access)
    const profile = await me()
    setUser(profile.data)
    return profile.data
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  return <AuthContext.Provider value={{ user, loading, login, logout }}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
