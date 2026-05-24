import { useEffect } from 'react'

export default function Toast({ msg, onClose }) {
  useEffect(() => {
    if (!msg) return
    const t = setTimeout(onClose, 2800)
    return () => clearTimeout(t)
  }, [msg, onClose])
  if (!msg) return null
  return (
    <div className={`toast show`}>
      <div className="toast-icon"><i className="ti ti-check" /></div>
      {msg}
    </div>
  )
}
