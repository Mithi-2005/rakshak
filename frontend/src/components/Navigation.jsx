import React, { useState } from 'react'
import { Link } from 'react-router-dom'

export default function Navigation({ isAuthenticated, setIsAuthenticated }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    setIsMenuOpen(false)
  }

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-accent-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">R</span>
            </div>
            <span className="hidden sm:inline text-xl font-bold bg-gradient-to-r from-primary-600 to-accent-600 bg-clip-text text-transparent">
              Rakshak
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-primary-600 font-medium transition">
              Home
            </Link>
            <Link to="/products" className="text-gray-700 hover:text-primary-600 font-medium transition">
              Products
            </Link>
            <Link to="/about" className="text-gray-700 hover:text-primary-600 font-medium transition">
              About
            </Link>
            <Link to="/quote" className="text-gray-700 hover:text-primary-600 font-medium transition">
              Get Quote
            </Link>
          </div>

          {/* Right Side Buttons/Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-primary-600 font-medium">
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="btn-primary"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button className="btn-secondary">
                  Sign In
                </button>
                <button className="btn-primary">
                  Sign Up
                </button>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={toggleMenu}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition text-2xl"
          >
            {isMenuOpen ? '✕' : '☰'}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden pb-4 space-y-3">
            <Link
              to="/"
              className="block px-4 py-2 text-gray-700 hover:bg-primary-50 rounded-lg transition"
              onClick={() => setIsMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              to="/products"
              className="block px-4 py-2 text-gray-700 hover:bg-primary-50 rounded-lg transition"
              onClick={() => setIsMenuOpen(false)}
            >
              Products
            </Link>
            <Link
              to="/about"
              className="block px-4 py-2 text-gray-700 hover:bg-primary-50 rounded-lg transition"
              onClick={() => setIsMenuOpen(false)}
            >
              About
            </Link>
            <Link
              to="/quote"
              className="block px-4 py-2 text-gray-700 hover:bg-primary-50 rounded-lg transition"
              onClick={() => setIsMenuOpen(false)}
            >
              Get Quote
            </Link>
            <div className="flex gap-2 px-4">
              {isAuthenticated ? (
                <>
                  <Link
                    to="/dashboard"
                    className="flex-1 btn-secondary text-center"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Dashboard
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="flex-1 btn-primary"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <button className="flex-1 btn-secondary">
                    Sign In
                  </button>
                  <button className="flex-1 btn-primary">
                    Sign Up
                  </button>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
