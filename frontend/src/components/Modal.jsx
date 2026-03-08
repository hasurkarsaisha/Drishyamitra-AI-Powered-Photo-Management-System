function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="indian-card relative z-10 w-full max-w-2xl max-h-[90vh] overflow-y-auto slide-up">
        {/* Header */}
        <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-orange-200">
          <h2 className="text-3xl font-bold text-maroon flex items-center gap-2">
            <span>✨</span>
            <span>{title}</span>
          </h2>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-full bg-gradient-to-r from-red-500 to-orange-500 text-white font-bold text-xl hover:scale-110 transition-transform"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div>{children}</div>

        {/* Footer Decoration */}
        <div className="flex items-center justify-center gap-2 mt-6 pt-4 border-t-2 border-orange-200">
          <span>🪔</span>
          <span className="text-sm text-gray-500">DrishyaMitra</span>
          <span>🪔</span>
        </div>
      </div>
    </div>
  )
}

export default Modal
