import React from 'react'
import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 py-12">
          {/* Brand Section */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-accent-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">R</span>
              </div>
              <span className="text-xl font-bold">Rakshak</span>
            </div>
            <p className="text-gray-400 text-sm mb-4">
              Protecting your future with transparent, affordable insurance solutions.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="hover:text-primary-500 transition text-2xl">
                👍
              </a>
              <a href="#" className="hover:text-primary-500 transition text-2xl">
                𝕏
              </a>
              <a href="#" className="hover:text-primary-500 transition text-2xl">
                💼
              </a>
              <a href="#" className="hover:text-primary-500 transition text-2xl">
                ✉️
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold mb-4 text-lg">Quick Links</h3>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-400 hover:text-primary-500 transition">Home</Link></li>
              <li><Link to="/products" className="text-gray-400 hover:text-primary-500 transition">Products</Link></li>
              <li><Link to="/about" className="text-gray-400 hover:text-primary-500 transition">About Us</Link></li>
              <li><Link to="/quote" className="text-gray-400 hover:text-primary-500 transition">Get Quote</Link></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="font-bold mb-4 text-lg">Support</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-primary-500 transition">Contact Us</a></li>
              <li><a href="#" className="text-gray-400 hover:text-primary-500 transition">FAQ</a></li>
              <li><a href="#" className="text-gray-400 hover:text-primary-500 transition">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-400 hover:text-primary-500 transition">Terms & Conditions</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-bold mb-4 text-lg">Contact</h3>
            <p className="text-gray-400 text-sm mb-2">📧 support@rakshak.com</p>
            <p className="text-gray-400 text-sm mb-2">📞 1-800-RAKSHAK</p>
            <p className="text-gray-400 text-sm mb-4">🕐 24/7 Customer Support</p>
            <input
              type="email"
              placeholder="Your email"
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-800"></div>

        {/* Bottom Section */}
        <div className="flex flex-col md:flex-row justify-between items-center py-8">
          <p className="text-gray-400 text-sm">
            © 2024 Rakshak. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a href="#" className="text-gray-400 hover:text-primary-500 text-sm transition">Privacy</a>
            <a href="#" className="text-gray-400 hover:text-primary-500 text-sm transition">Terms</a>
            <a href="#" className="text-gray-400 hover:text-primary-500 text-sm transition">Cookies</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
