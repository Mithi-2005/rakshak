import React, { useState } from 'react'

export default function GetQuote() {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    productType: 'health',
    age: '',
    city: '',
    dependents: '',
  })

  const [submitted, setSubmitted] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // Here you would send the form data to your backend
    console.log('Form Submitted:', formData)
    setSubmitted(true)
    setTimeout(() => setSubmitted(false), 5000)
  }

  return (
    <div className="w-full">
      {/* Header */}
      <section className="bg-gradient-to-r from-primary-500 to-accent-600 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Get Your Free Quote</h1>
          <p className="text-lg opacity-90 max-w-2xl mx-auto">
            Get a personalized insurance quote in just 2 minutes. No credit card required.
          </p>
        </div>
      </section>

      {/* Quick Stats */}
      <section className="bg-gray-50 py-8 px-4 sm:px-6 lg:px-8 border-b border-gray-200">
        <div className="max-w-7xl mx-auto grid grid-cols-3 gap-4 md:gap-8">
          <div className="text-center">
            <div className="text-2xl md:text-3xl font-bold text-primary-600">2 min</div>
            <p className="text-gray-600 text-sm md:text-base">Quote Process</p>
          </div>
          <div className="text-center">
            <div className="text-2xl md:text-3xl font-bold text-primary-600">0</div>
            <p className="text-gray-600 text-sm md:text-base">Hidden Charges</p>
          </div>
          <div className="text-center">
            <div className="text-2xl md:text-3xl font-bold text-primary-600">100%</div>
            <p className="text-gray-600 text-sm md:text-base">Free & Safe</p>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Form */}
            <div className="md:col-span-2">
              <div className="card">
                {submitted && (
                  <div className="mb-6 p-4 bg-green-50 border-l-4 border-green-500 rounded">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl text-green-600">✓</span>
                      <div>
                        <p className="font-bold text-green-900">Submitted Successfully!</p>
                        <p className="text-green-700 text-sm">We'll send you a personalized quote within 24 hours.</p>
                      </div>
                    </div>
                  </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Full Name & Email */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-bold text-gray-900 mb-2">
                        Full Name *
                      </label>
                      <input
                        type="text"
                        name="fullName"
                        value={formData.fullName}
                        onChange={handleChange}
                        className="input-field"
                        placeholder="John Doe"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-gray-900 mb-2">
                        Email Address *
                      </label>
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        className="input-field"
                        placeholder="john@example.com"
                        required
                      />
                    </div>
                  </div>

                  {/* Phone & Product Type */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-bold text-gray-900 mb-2">
                        Phone Number *
                      </label>
                      <input
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        className="input-field"
                        placeholder="+91 98765 43210"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-gray-900 mb-2">
                        Insurance Type *
                      </label>
                      <select
                        name="productType"
                        value={formData.productType}
                        onChange={handleChange}
                        className="input-field"
                      >
                        <option value="health">Health Insurance</option>
                        <option value="life">Life Insurance</option>
                        <option value="travel">Travel Insurance</option>
                      </select>
                    </div>
                  </div>

                  {/* Age & City */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-bold text-gray-900 mb-2">
                        Age *
                      </label>
                      <input
                        type="number"
                        name="age"
                        value={formData.age}
                        onChange={handleChange}
                        className="input-field"
                        placeholder="30"
                        min="18"
                        max="80"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-gray-900 mb-2">
                        City *
                      </label>
                      <input
                        type="text"
                        name="city"
                        value={formData.city}
                        onChange={handleChange}
                        className="input-field"
                        placeholder="Mumbai"
                        required
                      />
                    </div>
                  </div>

                  {/* Dependents */}
                  <div>
                    <label className="block text-sm font-bold text-gray-900 mb-2">
                      Number of Dependents
                    </label>
                    <select
                      name="dependents"
                      value={formData.dependents}
                      onChange={handleChange}
                      className="input-field"
                    >
                      <option value="">Select...</option>
                      <option value="0">None</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4 or more</option>
                    </select>
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    className="w-full btn-primary"
                  >
                    Get My Free Quote →
                  </button>

                  <p className="text-center text-sm text-gray-600">
                    By submitting, you agree to our Privacy Policy. We'll never share your data.
                  </p>
                </form>
              </div>
            </div>

            {/* Sidebar */}
            <div className="md:col-span-1">
              {/* Benefits */}
              <div className="card mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Why Get a Quote?</h3>
                <ul className="space-y-4">
                  {[
                    'Personalized Plans',
                    'Best Price Guarantee',
                    'Instant Comparison',
                    'Expert Guidance',
                    'No Commitment',
                    'Quick Processing',
                  ].map((benefit, index) => (
                    <li key={index} className="flex items-start space-x-3">
                      <span className="text-xl text-primary-500 flex-shrink-0 mt-0.5">✓</span>
                      <span className="text-gray-700">{benefit}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Support */}
              <div className="card bg-gradient-to-b from-primary-50 to-accent-50 border border-primary-100">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Need Help?</h3>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-gray-600">📞 Call us anytime</p>
                    <p className="font-bold text-primary-600">1-800-RAKSHAK</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">📧 Email us</p>
                    <p className="font-bold text-primary-600">support@rakshak.com</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">💬 Live Chat</p>
                    <p className="text-primary-600 text-sm">Available 24/7</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-100">
        <div className="max-w-4xl mx-auto">
          <h2 className="section-title text-center mb-12">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {[
              {
                question: 'How long does the quote take?',
                answer: 'Our quote process takes just 2 minutes. You\'ll get a personalized quote immediately after answering a few simple questions.'
              },
              {
                question: 'Is the quote free?',
                answer: 'Yes! Our quote is completely free with no hidden charges. There\'s no obligation to buy.'
              },
              {
                question: 'Will my data be safe?',
                answer: 'We take data security very seriously. Your information is encrypted and never shared with third parties without your consent.'
              },
              {
                question: 'Can I customize my plan?',
                answer: 'Absolutely! Once you get your quote, our experts can help you customize the plan according to your specific needs.'
              },
            ].map((faq, index) => (
              <div key={index} className="bg-white rounded-lg p-6 hover:shadow-md transition">
                <h3 className="font-bold text-gray-900 mb-2">{faq.question}</h3>
                <p className="text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
