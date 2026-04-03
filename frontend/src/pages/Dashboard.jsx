import React, { useState } from 'react'

export default function Dashboard({ isAuthenticated }) {
  const [activeTab, setActiveTab] = useState('policies')

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center max-w-md">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Sign In Required</h2>
          <p className="text-gray-600 mb-6">Please sign in to access your dashboard.</p>
          <button className="btn-primary w-full">
            Sign In
          </button>
        </div>
      </div>
    )
  }

  const policies = [
    {
      id: 'POL001',
      type: 'Health Insurance',
      name: 'Premium Health Plan',
      status: 'Active',
      coverage: '₹10 Lakh',
      premium: '₹599/month',
      startDate: '2024-01-15',
      expiryDate: '2025-01-14',
    },
    {
      id: 'POL002',
      type: 'Life Insurance',
      name: 'Term Life Plan',
      status: 'Active',
      coverage: '₹50 Lakh',
      premium: '₹199/month',
      startDate: '2023-06-20',
      expiryDate: '2033-06-19',
    },
  ]

  const claims = [
    {
      id: 'CLM001',
      date: '2024-03-10',
      type: 'Health',
      amount: '₹45,000',
      status: 'Approved',
      payout: '₹45,000',
    },
    {
      id: 'CLM002',
      date: '2024-02-05',
      type: 'Health',
      amount: '₹12,000',
      status: 'Processed',
      payout: '₹12,000',
    },
  ]

  return (
    <div className="w-full">
      {/* Header */}
      <section className="bg-gradient-to-r from-primary-500 to-accent-600 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h1 className="text-4xl font-bold mb-2">Welcome Back, Rajesh!</h1>
              <p className="opacity-90">Manage your insurance policies and claims</p>
            </div>
            <div className="flex gap-3">
              <button className="p-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg transition text-2xl">
                🔔
              </button>
              <button className="p-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg transition text-2xl">
                ⚙️
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Stats */}
      <section className="bg-gray-50 py-8 px-4 sm:px-6 lg:px-8 border-b">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="card">
            <p className="text-gray-600 text-sm mb-2">Active Policies</p>
            <div className="text-3xl font-bold text-primary-600">2</div>
          </div>
          <div className="card">
            <p className="text-gray-600 text-sm mb-2">Total Coverage</p>
            <div className="text-3xl font-bold text-primary-600">₹60 Lakh</div>
          </div>
          <div className="card">
            <p className="text-gray-600 text-sm mb-2">Monthly Premium</p>
            <div className="text-3xl font-bold text-accent-600">₹798</div>
          </div>
          <div className="card">
            <p className="text-gray-600 text-sm mb-2">Claims This Year</p>
            <div className="text-3xl font-bold text-green-600">2</div>
          </div>
        </div>
      </section>

      {/* Tabs */}
      <section className="bg-white sticky top-16 shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-8 overflow-x-auto">
            {[
              { id: 'policies', label: 'My Policies', icon: '📋' },
              { id: 'claims', label: 'My Claims', icon: '📋' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-4 font-medium whitespace-nowrap border-b-2 transition-all duration-200 flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'text-primary-600 border-primary-600'
                    : 'text-gray-600 border-transparent hover:text-gray-900'
                }`}
              >
                <span className="text-xl">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {activeTab === 'policies' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900">Your Insurance Policies</h2>
              <div className="grid gap-6">
                {policies.map((policy) => (
                  <div key={policy.id} className="card">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 items-center mb-4">
                      <div>
                        <p className="text-sm text-gray-600">Policy Type</p>
                        <p className="font-bold text-gray-900">{policy.type}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Policy Name</p>
                        <p className="font-bold text-gray-900">{policy.name}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Coverage</p>
                        <p className="font-bold text-gray-900">{policy.coverage}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Premium</p>
                        <p className="font-bold text-gray-900">{policy.premium}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Status</p>
                        <span className="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                          {policy.status}
                        </span>
                      </div>
                      <div className="flex gap-2">
                        <button className="flex-1 p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition flex items-center justify-center gap-2">
                          <span className="text-xl">⬇️</span>
                          <span className="hidden sm:inline text-sm">Download</span>
                        </button>
                      </div>
                    </div>
                    <div className="border-t pt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600">Policy ID</p>
                        <p className="font-medium text-gray-900">{policy.id}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Start Date</p>
                        <p className="font-medium text-gray-900">{policy.startDate}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Expiry Date</p>
                        <p className="font-medium text-gray-900">{policy.expiryDate}</p>
                      </div>
                      <div>
                        <button className="text-primary-600 hover:text-primary-700 font-medium">
                          View Details →
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'claims' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900">Your Claims</h2>
                <button className="btn-primary">
                  File New Claim
                </button>
              </div>
              <div className="grid gap-6">
                {claims.length > 0 ? (
                  claims.map((claim) => (
                    <div key={claim.id} className="card">
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 items-center">
                        <div>
                          <p className="text-sm text-gray-600">Claim ID</p>
                          <p className="font-bold text-gray-900">{claim.id}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Date</p>
                          <p className="font-bold text-gray-900">{claim.date}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Type</p>
                          <p className="font-bold text-gray-900">{claim.type}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Amount</p>
                          <p className="font-bold text-gray-900">{claim.amount}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Status</p>
                          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                            claim.status === 'Approved'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-blue-100 text-blue-800'
                          }`}>
                            {claim.status}
                          </span>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Payout</p>
                          <p className="font-bold text-green-600">{claim.payout}</p>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-12">
                    <p className="text-gray-600 text-lg">No claims yet</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Quick Actions */}
      <section className="bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 mb-8">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <button className="card text-center hover:shadow-lg transition">
              <div className="text-4xl mb-4">📋</div>
              <h3 className="font-bold text-gray-900 mb-2">View Policy</h3>
              <p className="text-gray-600 text-sm">Detailed policy information</p>
            </button>
            <button className="card text-center hover:shadow-lg transition">
              <div className="text-4xl mb-4">🩹</div>
              <h3 className="font-bold text-gray-900 mb-2">File Claim</h3>
              <p className="text-gray-600 text-sm">Submit a new claim</p>
            </button>
            <button className="card text-center hover:shadow-lg transition">
              <div className="text-4xl mb-4">💳</div>
              <h3 className="font-bold text-gray-900 mb-2">Pay Premium</h3>
              <p className="text-gray-600 text-sm">Manage premiums</p>
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}
