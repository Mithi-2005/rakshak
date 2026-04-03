import api from './api'

export const quoteService = {
  // Get a quote
  getQuote: async (formData) => {
    try {
      const response = await api.post('/quotes', formData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // List all quotes
  getQuotes: async () => {
    try {
      const response = await api.get('/quotes')
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Get specific quote
  getQuoteById: async (quoteId) => {
    try {
      const response = await api.get(`/quotes/${quoteId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },
}

export const authService = {
  // Sign up
  signup: async (userData) => {
    try {
      const response = await api.post('/auth/signup', userData)
      if (response.data.token) {
        localStorage.setItem('authToken', response.data.token)
      }
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Sign in
  signin: async (credentials) => {
    try {
      const response = await api.post('/auth/signin', credentials)
      if (response.data.token) {
        localStorage.setItem('authToken', response.data.token)
      }
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Sign out
  signout: () => {
    localStorage.removeItem('authToken')
  },

  // Get current user
  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/me')
      return response.data
    } catch (error) {
      throw error
    }
  },
}

export const policyService = {
  // List all policies
  getPolicies: async () => {
    try {
      const response = await api.get('/policies')
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Get specific policy
  getPolicyById: async (policyId) => {
    try {
      const response = await api.get(`/policies/${policyId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Create new policy
  createPolicy: async (policyData) => {
    try {
      const response = await api.post('/policies', policyData)
      return response.data
    } catch (error) {
      throw error
    }
  },
}

export const claimService = {
  // List all claims
  getClaims: async () => {
    try {
      const response = await api.get('/claims')
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Get specific claim
  getClaimById: async (claimId) => {
    try {
      const response = await api.get(`/claims/${claimId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // File new claim
  fileClaim: async (claimData) => {
    try {
      const response = await api.post('/claims', claimData)
      return response.data
    } catch (error) {
      throw error
    }
  },
}
