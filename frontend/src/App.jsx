import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import Footer from './components/Footer'
import Home from './pages/Home'
import Products from './pages/Products'
import About from './pages/About'
import GetQuote from './pages/GetQuote'
import Dashboard from './pages/Dashboard'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-gray-50">
        <Navigation isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<Products />} />
            <Route path="/about" element={<About />} />
            <Route path="/quote" element={<GetQuote />} />
            <Route path="/dashboard" element={<Dashboard isAuthenticated={isAuthenticated} />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
