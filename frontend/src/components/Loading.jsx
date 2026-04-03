import React from 'react'

export default function Loading({ message = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative w-12 h-12 mb-4">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-accent-600 rounded-full animate-spin"
          style={{
            backgroundClip: 'padding-box',
            WebkitMaskImage: 'radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 2px))',
            maskImage: 'radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 2px))',
          }}>
        </div>
      </div>
      <p className="text-gray-600 font-medium">{message}</p>
    </div>
  )
}
