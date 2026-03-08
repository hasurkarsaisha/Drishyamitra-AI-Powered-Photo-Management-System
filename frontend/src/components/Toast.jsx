import { useEffect } from 'react'

function Toast({ message, type = 'success', onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose()
    }, 3000)

    return () => clearTimeout(timer)
  }, [onClose])

  const styles = {
    success: 'bg-gradient-to-r from-green-500 to-emerald-500 border-green-600',
    error: 'bg-gradient-to-r from-red-500 to-orange-500 border-red-600',
    info: 'bg-gradient-to-r from-blue-500 to-cyan-500 border-blue-600'
  }

  const icons = {
    success: '✅',
    error: '❌',
    info: 'ℹ️'
  }

  return (
    <div className="fixed top-4 right-4 z-50 animate-slide-in">
      <div className={`${styles[type]} text-white px-6 py-4 rounded-xl shadow-2xl border-2 flex items-center gap-3 min-w-[300px] diya-glow`}>
        <span className="text-2xl">{icons[type]}</span>
        <p className="font-semibold flex-1">{message}</p>
        <button
          onClick={onClose}
          className="text-white hover:text-gray-200 font-bold text-xl"
        >
          ×
        </button>
      </div>
    </div>
  )
}

export default Toast
