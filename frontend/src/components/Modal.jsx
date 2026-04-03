import React from 'react'

export default function Modal({ 
  isOpen, 
  onClose, 
  title, 
  children,
  footer,
  size = 'md'
}) {
  if (!isOpen) return null

  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
  }

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className={`bg-white rounded-lg shadow-xl ${sizes[size]} w-full max-h-[90vh] overflow-y-auto`}>
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200 sticky top-0 bg-white">
            <h2 className="text-xl font-bold text-gray-900">{title}</h2>
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 rounded-lg transition text-2xl text-gray-600"
            >
              ✕
            </button>
          </div>

          {/* Content */}
          <div className="p-6">
            {children}
          </div>

          {/* Footer */}
          {footer && (
            <div className="border-t border-gray-200 p-6 bg-gray-50 flex gap-3 justify-end sticky bottom-0">
              {footer}
            </div>
          )}
        </div>
      </div>
    </>
  )
}
