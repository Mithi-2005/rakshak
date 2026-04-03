import React from 'react'
import { Link } from 'react-router-dom'

export default function Home() {
  const features = [
    {
      icon: '🛡️',
      title: 'Secure Protection',
      description: 'Comprehensive coverage with industry-leading security standards'
    },
    {
      icon: '⚡',
      title: 'Quick Claims',
      description: 'Fast and hassle-free claim processing within 24 hours'
    },
    {
      icon: '💰',
      title: 'Affordable Rates',
      description: 'Transparent pricing with no hidden charges or fees'
    },
    {
      icon: '👥',
      title: '24/7 Support',
      description: 'Expert customer support available round the clock'
    },
  ]

  const testimonials = [
    {
      name: 'Raj Kumar',
      role: 'Business Owner',
      content: 'Rakshak made insurance shopping incredibly easy. Best decision!',
      rating: 5
    },
    {
      name: 'Priya Sharma',
      role: 'Software Engineer',
      content: 'Transparent pricing and quick claim settlement. Highly recommended!',
      rating: 5
    },
    {
      name: 'Amit Patel',
      role: 'Entrepreneur',
      content: 'Great customer service and affordable plans. Very satisfied!',
      rating: 4
    },
  ]

  return (
    <div className="w-full">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-500 via-accent-500 to-primary-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-6">
              <h1 className="text-4xl md:text-5xl font-bold leading-tight">
                Protect Your Future with Rakshak
              </h1>
              <p className="text-lg md:text-xl opacity-90">
                Simple, transparent, and affordable insurance solutions tailored for you. Get comprehensive coverage in just minutes.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/quote"
                  className="inline-flex items-center justify-center px-8 py-3 bg-white text-primary-600 font-bold rounded-lg hover:shadow-lg transition-all duration-200 hover:scale-105"
                >
                  Get Free Quote →
                </Link>
                <Link
                  to="/products"
                  className="inline-flex items-center justify-center px-8 py-3 border-2 border-white text-white font-bold rounded-lg hover:bg-white hover:text-primary-600 transition-all duration-200"
                >
                  Explore Products
                </Link>
              </div>
            </div>

            {/* Right Image/Illustration */}
            <div className="hidden md:block">
              <div className="bg-white bg-opacity-10 rounded-2xl p-8 backdrop-blur-sm">
                <div className="text-center">
                  <div className="text-4xl mx-auto mb-4">🛡️</div>
                  <p className="text-xl font-semibold">Trusted by 50,000+ Customers</p>
                </div>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16 pt-12 border-t border-white border-opacity-20">
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">50K+</div>
              <p className="opacity-90">Happy Customers</p>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">₹100Cr+</div>
              <p className="opacity-90">Claims Settled</p>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">24h</div>
              <p className="opacity-90">Claim Processing</p>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">10+</div>
              <p className="opacity-90">Insurance Plans</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="section-title">Why Choose Rakshak?</h2>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              We believe insurance should be simple, transparent, and accessible to everyone.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="card group">
                <div className="text-4xl mb-4 group-hover:scale-110 transition-transform inline-block">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2 text-gray-900">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Products Preview */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-100">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="section-title">Our Insurance Products</h2>
            <p className="text-gray-600 text-lg">Choose the perfect plan for your needs</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            {[
              { title: 'Health Insurance', price: '₹299/mo', features: ['Comprehensive Coverage', 'Cashless Treatment', 'Pre/Post Hospitalization'] },
              { title: 'Life Insurance', price: '₹199/mo', features: ['Lifetime Payout', 'Income Protection', 'Family Security'], highlight: true },
              { title: 'Travel Insurance', price: '₹399/yr', features: ['Global Coverage', 'Medical Emergencies', 'Trip Protection'] },
            ].map((product, index) => (
              <div
                key={index}
                className={`rounded-xl p-8 transition-all duration-200 ${
                  product.highlight
                    ? 'bg-gradient-to-r from-primary-500 to-accent-600 text-white shadow-xl scale-105'
                    : 'bg-white shadow-md hover:shadow-lg'
                }`}
              >
                <h3 className={`text-2xl font-bold mb-2 ${product.highlight ? 'text-white' : 'text-gray-900'}`}>
                  {product.title}
                </h3>
                <div className={`text-3xl font-bold mb-6 ${product.highlight ? 'text-white' : 'text-primary-500'}`}>
                  {product.price}
                </div>
                <ul className="space-y-3 mb-8">
                  {product.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center space-x-2">
                      <span className={`w-1.5 h-1.5 rounded-full ${product.highlight ? 'bg-white' : 'bg-primary-500'}`}></span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
                <button
                  className={`w-full py-2 rounded-lg font-bold transition-all duration-200 ${
                    product.highlight
                      ? 'bg-white text-primary-600 hover:shadow-lg'
                      : 'bg-gradient-to-r from-primary-500 to-accent-600 text-white hover:shadow-lg'
                  }`}
                >
                  Get Quote
                </button>
              </div>
            ))}
          </div>
          <div className="text-center">
            <Link to="/products" className="btn-primary">
              View All Plans →
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="section-title">What Our Customers Say</h2>
            <p className="text-gray-600 text-lg">Real experiences from real people</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="card">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-primary-500 to-accent-600 flex items-center justify-center text-white font-bold mr-4">
                    {testimonial.name.charAt(0)}
                  </div>
                  <div>
                    <p className="font-bold text-gray-900">{testimonial.name}</p>
                    <p className="text-sm text-gray-600">{testimonial.role}</p>
                  </div>
                </div>
                <p className="text-gray-600 mb-4">"{testimonial.content}"</p>
                <div className="flex">
                  {Array.from({ length: testimonial.rating }).map((_, i) => (
                    <span key={i} className="text-accent-500 text-lg">★</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-primary-600 to-accent-600 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h2 className="text-4xl font-bold">Ready to Protect Your Future?</h2>
          <p className="text-lg opacity-90">
            Get a free quote in just 2 minutes. No credit card required.
          </p>
          <Link
            to="/quote"
            className="inline-block px-8 py-3 bg-white text-primary-600 font-bold rounded-lg hover:shadow-lg transition-all duration-200 hover:scale-105"
          >
            Get Your Free Quote Now →
          </Link>
        </div>
      </section>
    </div>
  )
}
