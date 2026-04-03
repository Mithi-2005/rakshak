import React, { useState } from 'react'

export default function Products() {
  const [activeTab, setActiveTab] = useState('health')

  const products = {
    health: {
      name: 'Health Insurance',
      description: 'Comprehensive health coverage for you and your family',
      plans: [
        {
          name: 'Basic Plan',
          price: '₹299',
          period: '/month',
          coverage: '₹5 Lakh',
          features: [
            { name: 'Hospitalization', included: true },
            { name: 'Day Care', included: true },
            { name: 'Pre-existing diseases', included: false },
            { name: 'Annual Health Check-up', included: false },
            { name: 'Cashless Treatment', included: true },
          ]
        },
        {
          name: 'Premium Plan',
          price: '₹599',
          period: '/month',
          coverage: '₹10 Lakh',
          highlight: true,
          features: [
            { name: 'Hospitalization', included: true },
            { name: 'Day Care', included: true },
            { name: 'Pre-existing diseases', included: true },
            { name: 'Annual Health Check-up', included: true },
            { name: 'Cashless Treatment', included: true },
          ]
        },
        {
          name: 'Elite Plan',
          price: '₹999',
          period: '/month',
          coverage: '₹20 Lakh',
          features: [
            { name: 'Hospitalization', included: true },
            { name: 'Day Care', included: true },
            { name: 'Pre-existing diseases', included: true },
            { name: 'Annual Health Check-up', included: true },
            { name: 'Cashless Treatment', included: true },
          ]
        },
      ]
    },
    life: {
      name: 'Life Insurance',
      description: 'Secure your family\'s financial future',
      plans: [
        {
          name: 'Term Plan',
          price: '₹199',
          period: '/month',
          coverage: '₹50 Lakh',
          features: [
            { name: 'Death Benefit', included: true },
            { name: 'Critical Illness', included: true },
            { name: 'Disability Cover', included: false },
            { name: 'Accidental Death', included: true },
            { name: 'Loan against Policy', included: false },
          ]
        },
        {
          name: 'Whole Life Plan',
          price: '₹499',
          period: '/month',
          coverage: '₹50 Lakh',
          highlight: true,
          features: [
            { name: 'Death Benefit', included: true },
            { name: 'Critical Illness', included: true },
            { name: 'Disability Cover', included: true },
            { name: 'Accidental Death', included: true },
            { name: 'Loan against Policy', included: true },
          ]
        },
        {
          name: 'Child Future Plan',
          price: '₹399',
          period: '/month',
          coverage: '₹25 Lakh',
          features: [
            { name: 'Death Benefit', included: true },
            { name: 'Maturity Benefit', included: true },
            { name: 'Educational Support', included: true },
            { name: 'Accidental Death', included: true },
            { name: 'Premium Waiver', included: true },
          ]
        },
      ]
    },
    travel: {
      name: 'Travel Insurance',
      description: 'Travel with confidence, anywhere in the world',
      plans: [
        {
          name: 'Domestic Trip',
          price: '₹99',
          period: '/trip',
          coverage: 'All India',
          features: [
            { name: 'Medical Emergencies', included: true },
            { name: 'Trip Cancellation', included: true },
            { name: 'Lost Luggage', included: true },
            { name: 'Travel Delays', included: false },
            { name: 'Hotel Accommodation', included: false },
          ]
        },
        {
          name: 'International Trip',
          price: '₹399',
          period: '/trip',
          coverage: 'Worldwide',
          highlight: true,
          features: [
            { name: 'Medical Emergencies', included: true },
            { name: 'Trip Cancellation', included: true },
            { name: 'Lost Luggage', included: true },
            { name: 'Travel Delays', included: true },
            { name: 'Hotel Accommodation', included: true },
          ]
        },
        {
          name: 'Visa Travel',
          price: '₹249',
          period: '/trip',
          coverage: 'Visa Countries',
          features: [
            { name: 'Medical Emergencies', included: true },
            { name: 'Trip Cancellation', included: true },
            { name: 'Lost Luggage', included: true },
            { name: 'Travel Delays', included: true },
            { name: 'Hotel Accommodation', included: false },
          ]
        },
      ]
    }
  }

  const currentProduct = products[activeTab]

  return (
    <div className="w-full">
      {/* Header */}
      <section className="bg-gradient-to-r from-primary-500 to-accent-600 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Our Insurance Products</h1>
          <p className="text-lg opacity-90 max-w-2xl mx-auto">
            Choose from our wide range of insurance plans designed for every need and budget.
          </p>
        </div>
      </section>

      {/* Product Navigation */}
      <section className="bg-white sticky top-16 shadow-md py-4 px-4 sm:px-6 lg:px-8 z-40">
        <div className="max-w-7xl mx-auto">
          <div className="flex gap-2 md:gap-4 overflow-x-auto pb-2">
            {Object.keys(products).map((key) => (
              <button
                key={key}
                onClick={() => setActiveTab(key)}
                className={`px-4 md:px-6 py-2 font-medium whitespace-nowrap transition-all duration-200 rounded-lg ${
                  activeTab === key
                    ? 'bg-gradient-to-r from-primary-500 to-accent-600 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                {products[key].name}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Product Details & Plans */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="mb-12">
            <h2 className="section-title">{currentProduct.name}</h2>
            <p className="text-gray-600 text-lg">{currentProduct.description}</p>
          </div>

          {/* Plans Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {currentProduct.plans.map((plan, index) => (
              <div
                key={index}
                className={`transition-all duration-200 rounded-xl overflow-hidden ${
                  plan.highlight
                    ? 'ring-2 ring-primary-500 shadow-xl scale-105'
                    : 'shadow-md hover:shadow-lg'
                }`}
              >
                <div
                  className={`p-8 ${
                    plan.highlight
                      ? 'bg-gradient-to-r from-primary-500 to-accent-600 text-white'
                      : 'bg-white'
                  }`}
                >
                  {plan.highlight && (
                    <div className="inline-block bg-white text-primary-600 px-3 py-1 rounded-full text-sm font-bold mb-4">
                      Most Popular
                    </div>
                  )}
                  <h3 className={`text-2xl font-bold mb-2 ${plan.highlight ? 'text-white' : 'text-gray-900'}`}>
                    {plan.name}
                  </h3>
                  <div className={`text-sm mb-4 ${plan.highlight ? 'text-white text-opacity-90' : 'text-gray-600'}`}>
                    Coverage: <strong>{plan.coverage}</strong>
                  </div>
                  <div className="relative">
                    <span className={`text-4xl font-bold ${plan.highlight ? 'text-white' : 'text-primary-600'}`}>
                      {plan.price}
                    </span>
                    <span className={plan.highlight ? 'text-white text-opacity-90' : 'text-gray-600'}>
                      {plan.period}
                    </span>
                  </div>
                </div>

                <div className={`p-8 ${plan.highlight ? 'bg-white' : 'bg-gray-50'}`}>
                  <ul className="space-y-4 mb-8">
                    {plan.features.map((feature, idx) => (
                      <li key={idx} className="flex items-center space-x-3">
                        <span className={`text-xl flex-shrink-0 ${
                          feature.included
                            ? plan.highlight ? 'text-primary-500' : 'text-green-500'
                            : 'text-gray-300'
                        }`}>
                          {feature.included ? '✓' : '✕'}
                        </span>
                        <span
                          className={
                            feature.included
                              ? 'text-gray-900'
                              : 'text-gray-400'
                          }
                        >
                          {feature.name}
                        </span>
                      </li>
                    ))}
                  </ul>
                  <button
                    className={`w-full py-3 rounded-lg font-bold transition-all duration-200 ${
                      plan.highlight
                        ? 'bg-gradient-to-r from-primary-500 to-accent-600 text-white hover:shadow-lg'
                        : 'bg-white border-2 border-primary-500 text-primary-500 hover:bg-primary-50'
                    }`}
                  >
                    Get Quote
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Comparison Table */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-100">
        <div className="max-w-7xl mx-auto">
          <h2 className="section-title text-center mb-12">Plan Comparison</h2>
          <div className="bg-white rounded-xl shadow-lg overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gradient-to-r from-primary-500 to-accent-600 text-white">
                <tr>
                  <th className="px-6 py-4 text-left font-bold">Features</th>
                  {currentProduct.plans.map((plan, idx) => (
                    <th key={idx} className="px-6 py-4 text-center font-bold">
                      {plan.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {currentProduct.plans[0].features.map((_, featureIdx) => (
                  <tr key={featureIdx} className="border-b border-gray-200">
                    <td className="px-6 py-4 font-medium text-gray-900">
                      {currentProduct.plans[0].features[featureIdx].name}
                    </td>
                    {currentProduct.plans.map((plan, planIdx) => (
                      <td key={planIdx} className="px-6 py-4 text-center">
                        {plan.features[featureIdx].included ? (
                          <Check className="w-5 h-5 mx-auto text-green-500" />
                        ) : (
                          <X className="w-5 h-5 mx-auto text-gray-300" />
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-primary-600 to-accent-600 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h2 className="text-4xl font-bold">Still have questions?</h2>
          <p className="text-lg opacity-90">
            Our insurance experts are here to help you choose the best plan.
          </p>
          <button className="inline-block px-8 py-3 bg-white text-primary-600 font-bold rounded-lg hover:shadow-lg transition-all duration-200 hover:scale-105">
            Contact Our Experts
          </button>
        </div>
      </section>
    </div>
  )
}
