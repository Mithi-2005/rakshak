import React from 'react'

export default function Alert({ type = 'info', title, message, onClose }) {
  const icons = {
    success: '✓',
    error: '⚠️',
    warning: '⚠️',
    info: 'ℹ️',
  }

  const colors = {
    success: 'bg-green-50 border-l-4 border-green-500',
    error: 'bg-red-50 border-l-4 border-red-500',
    warning: 'bg-yellow-50 border-l-4 border-yellow-500',
    info: 'bg-blue-50 border-l-4 border-blue-500',
  }

  const textColors = {
    success: 'text-green-900',
    error: 'text-red-900',
    warning: 'text-yellow-900',
    info: 'text-blue-900',
  }

  return (
    <div className={`${colors[type]} p-4 rounded flex items-start gap-3 mb-4`}>
      <div className={`text-xl flex-shrink-0 ${textColors[type]}`}>{icons[type]}</div>
      <div className="flex-1">
        {title && <p className={`font-bold ${textColors[type]}`}>{title}</p>}
        {message && <p className={`text-sm ${textColors[type]} mt-1`}>{message}</p>}
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className={`flex-shrink-0 ${textColors[type]} hover:opacity-70 text-xl`}
        >
          ✕
        </button>
      )}
    </div>
  )
}
