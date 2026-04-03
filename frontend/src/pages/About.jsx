import React from 'react'

export default function About() {
  const values = [
    {
      icon: '❤️',
      title: 'Customer First',
      description: 'We prioritize transparency and customer satisfaction in everything we do.'
    },
    {
      icon: '🎯',
      title: 'Mission Driven',
      description: 'Making insurance accessible and affordable for every Indian family.'
    },
    {
      icon: '⚡',
      title: 'Innovation',
      description: 'Leveraging technology to provide fast, seamless insurance solutions.'
    },
    {
      icon: '👥',
      title: 'Community',
      description: 'Building a community of protected individuals and families.'
    },
  ]

  const team = [
    {
      name: 'Arjun Singh',
      role: 'Founder & CEO',
      bio: '15+ years in insurance industry'
    },
    {
      name: 'Priya Verma',
      role: 'Head of Operations',
      bio: '12+ years financial services background'
    },
    {
      name: 'Rajesh Patel',
      role: 'Chief Technology Officer',
      bio: 'Ex-Google engineer, AI & fintech expert'
    },
    {
      name: 'Neha Sharma',
      role: 'Head of Customer Experience',
      bio: '10+ years customer service excellence'
    },
  ]

  return (
    <div className="w-full">
      {/* Header */}
      <section className="bg-gradient-to-r from-primary-500 to-accent-600 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">About Rakshak</h1>
          <p className="text-lg opacity-90 max-w-2xl mx-auto">
            Simplifying insurance for millions of Indians
          </p>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-16">
            <div>
              <h2 className="section-title">Our Mission</h2>
              <p className="text-gray-600 text-lg leading-relaxed mb-6">
                At Rakshak, we believe that everyone deserves access to transparent, affordable, and reliable insurance. Our mission is to simplify the insurance buying process and protect millions of Indian families from financial uncertainties.
              </p>
              <p className="text-gray-600 text-lg leading-relaxed">
                We're committed to eliminating complexity from insurance and making it a seamless experience for everyone.
              </p>
            </div>
            <div className="bg-gradient-to-br from-primary-100 to-accent-100 rounded-xl p-8 text-center">
              <div className="text-5xl font-bold text-primary-600 mb-2">10M+</div>
              <p className="text-gray-700">Lives Protected Since 2019</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div className="bg-gradient-to-br from-accent-100 to-primary-100 rounded-xl p-8 text-center">
              <div className="text-5xl font-bold text-accent-600 mb-2">₹500Cr+</div>
              <p className="text-gray-700">Claims Processed & Paid</p>
            </div>
            <div>
              <h2 className="section-title">Our Vision</h2>
              <p className="text-gray-600 text-lg leading-relaxed mb-6">
                We envision a future where insurance is not seen as a burden but as an empowering tool that gives people peace of mind and financial security.
              </p>
              <p className="text-gray-600 text-lg leading-relaxed">
                By combining cutting-edge technology with human expertise, we're building the insurance platform of the future.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Core Values */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-100">
        <div className="max-w-7xl mx-auto">
          <h2 className="section-title text-center mb-12">Our Core Values</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <div key={index} className="card bg-white">
                <div className="text-4xl mb-4">{value.icon}</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{value.title}</h3>
                <p className="text-gray-600">{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="section-title text-center mb-12">Our Journey</h2>
          <div className="space-y-8">
            {[
              { year: '2019', title: 'Rakshak Founded', description: 'Started with a vision to revolutionize insurance in India' },
              { year: '2020', title: 'First 1 Lakh Customers', description: 'Rapid growth and customer trust during challenging times' },
              { year: '2021', title: 'Multi-Product Launch', description: 'Expanded from health to life and travel insurance' },
              { year: '2022', title: '10 Million Lives Protected', description: 'Became one of India\'s fastest-growing insurtech platforms' },
              { year: '2023', title: 'AI Innovation', description: 'Introduced AI-powered quote generation and claim processing' },
              { year: '2024', title: 'Global Expansion', description: 'Started international operations with South Asian markets' },
            ].map((milestone, index) => (
              <div key={index} className="flex gap-6">
                <div className="flex flex-col items-center">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-primary-500 to-accent-600 flex items-center justify-center text-white font-bold text-sm">
                    {index + 1}
                  </div>
                  {index !== 5 && (
                    <div className="w-1 h-16 bg-gradient-to-b from-primary-500 to-gray-300 mt-2"></div>
                  )}
                </div>
                <div className="pb-8">
                  <div className="flex items-baseline gap-4 mb-2">
                    <span className="text-2xl font-bold text-primary-600">{milestone.year}</span>
                    <h3 className="text-xl font-bold text-gray-900">{milestone.title}</h3>
                  </div>
                  <p className="text-gray-600">{milestone.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-100">
        <div className="max-w-7xl mx-auto">
          <h2 className="section-title text-center mb-12">Meet Our Leadership Team</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <div key={index} className="card bg-white text-center">
                <div className="w-24 h-24 rounded-full bg-gradient-to-r from-primary-500 to-accent-600 mx-auto mb-4 flex items-center justify-center text-white text-3xl font-bold">
                  {member.name.charAt(0)}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-1">{member.name}</h3>
                <p className="text-primary-600 font-semibold mb-3">{member.role}</p>
                <p className="text-gray-600 text-sm">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Awards & Recognition */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="section-title text-center mb-12">Awards & Recognition</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {[
              { award: 'Best InsurTech', org: 'India Tech Awards 2023' },
              { award: 'Most Trusted Brand', org: 'Customer Choice 2023' },
              { award: 'Innovation Leader', org: 'FinTech India 2022' },
              { award: 'Fast 50 Company', org: 'Deloitte 2021' },
            ].map((item, index) => (
              <div key={index} className="card">
                <p className="text-primary-600 font-bold mb-2">🏆</p>
                <p className="font-bold text-gray-900 mb-2">{item.award}</p>
                <p className="text-gray-600 text-sm">{item.org}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact CTA */}
      <section className="bg-gradient-to-r from-primary-600 to-accent-600 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h2 className="text-4xl font-bold">Get In Touch</h2>
          <p className="text-lg opacity-90">
            Have questions about Rakshak? We'd love to hear from you!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-3 bg-white text-primary-600 font-bold rounded-lg hover:shadow-lg transition-all duration-200">
              Contact Us
            </button>
            <button className="px-8 py-3 border-2 border-white text-white font-bold rounded-lg hover:bg-white hover:text-primary-600 transition-all duration-200">
              Careers
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}
