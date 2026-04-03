// Product Types
export const PRODUCTS = {
  HEALTH: 'health',
  LIFE: 'life',
  TRAVEL: 'travel',
}

export const PRODUCT_NAMES = {
  health: 'Health Insurance',
  life: 'Life Insurance',
  travel: 'Travel Insurance',
}

// Claim Status
export const CLAIM_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  PROCESSED: 'processed',
}

export const CLAIM_STATUS_COLORS = {
  pending: 'yellow',
  approved: 'green',
  rejected: 'red',
  processed: 'blue',
}

// Policy Status
export const POLICY_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  EXPIRED: 'expired',
}

// API Endpoints
export const API_ENDPOINTS = {
  // Auth
  SIGNUP: '/auth/signup',
  SIGNIN: '/auth/signin',
  LOGOUT: '/auth/logout',
  GET_USER: '/auth/me',

  // Quotes
  GET_QUOTES: '/quotes',
  CREATE_QUOTE: '/quotes',
  GET_QUOTE: (id) => `/quotes/${id}`,

  // Policies
  GET_POLICIES: '/policies',
  CREATE_POLICY: '/policies',
  GET_POLICY: (id) => `/policies/${id}`,
  UPDATE_POLICY: (id) => `/policies/${id}`,

  // Claims
  GET_CLAIMS: '/claims',
  CREATE_CLAIM: '/claims',
  GET_CLAIM: (id) => `/claims/${id}`,
  UPDATE_CLAIM: (id) => `/claims/${id}`,
}

// Insurance Plans
export const HEALTH_PLANS = [
  {
    id: 'health-basic',
    name: 'Basic Plan',
    price: 299,
    coverage: 500000,
    features: ['Hospitalization', 'Day Care', 'Cashless Treatment'],
  },
  {
    id: 'health-premium',
    name: 'Premium Plan',
    price: 599,
    coverage: 1000000,
    features: ['All Basic Features', 'Pre-existing diseases', 'Health Check-up'],
    popular: true,
  },
  {
    id: 'health-elite',
    name: 'Elite Plan',
    price: 999,
    coverage: 2000000,
    features: ['All Premium Features', 'Advanced Coverage', 'Priority Support'],
  },
]

// Validation Rules
export const VALIDATION = {
  EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE_REGEX: /^[0-9]{10}$/,
  MIN_AGE: 18,
  MAX_AGE: 80,
}

// Messages
export const MESSAGES = {
  SUCCESS: {
    QUOTE_GENERATED: 'Quote generated successfully!',
    POLICY_CREATED: 'Policy created successfully!',
    CLAIM_FILED: 'Claim filed successfully!',
  },
  ERROR: {
    GENERIC: 'Something went wrong. Please try again.',
    NETWORK: 'Network error. Please check your connection.',
    VALIDATION: 'Please fill all required fields.',
  },
}

// Routes
export const ROUTES = {
  HOME: '/',
  PRODUCTS: '/products',
  ABOUT: '/about',
  QUOTE: '/quote',
  DASHBOARD: '/dashboard',
  LOGIN: '/login',
  SIGNUP: '/signup',
}
