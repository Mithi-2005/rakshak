// Form validation utilities
export const validators = {
  // Email validation
  email: (value) => {
    if (!value) return 'Email is required'
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) return 'Invalid email address'
    return null
  },

  // Phone validation
  phone: (value) => {
    if (!value) return 'Phone number is required'
    const phoneRegex = /^[0-9]{10}$/
    const cleaned = value.replace(/\D/g, '')
    if (!phoneRegex.test(cleaned)) return 'Phone must be 10 digits'
    return null
  },

  // Name validation
  name: (value) => {
    if (!value) return 'Name is required'
    if (value.trim().length < 2) return 'Name must be at least 2 characters'
    return null
  },

  // Age validation
  age: (value, minAge = 18, maxAge = 80) => {
    if (!value) return 'Age is required'
    const age = parseInt(value)
    if (age < minAge) return `Age must be at least ${minAge}`
    if (age > maxAge) return `Age must not exceed ${maxAge}`
    return null
  },

  // Password validation
  password: (value) => {
    if (!value) return 'Password is required'
    if (value.length < 8) return 'Password must be at least 8 characters'
    if (!/[A-Z]/.test(value)) return 'Password must contain uppercase letter'
    if (!/[a-z]/.test(value)) return 'Password must contain lowercase letter'
    if (!/[0-9]/.test(value)) return 'Password must contain a number'
    return null
  },

  // Confirm password validation
  confirmPassword: (value, password) => {
    if (!value) return 'Please confirm your password'
    if (value !== password) return 'Passwords do not match'
    return null
  },

  // URL validation
  url: (value) => {
    if (!value) return 'URL is required'
    try {
      new URL(value)
      return null
    } catch {
      return 'Invalid URL'
    }
  },

  // Number validation
  number: (value, min = 0, max = Infinity) => {
    if (value === '') return 'This field is required'
    const num = parseFloat(value)
    if (isNaN(num)) return 'Must be a valid number'
    if (num < min) return `Must be at least ${min}`
    if (num > max) return `Must not exceed ${max}`
    return null
  },

  // Required field validation
  required: (value) => {
    if (!value || (typeof value === 'string' && !value.trim())) {
      return 'This field is required'
    }
    return null
  },

  // Min length validation
  minLength: (value, length) => {
    if (!value) return 'This field is required'
    if (value.length < length) return `Must be at least ${length} characters`
    return null
  },

  // Max length validation
  maxLength: (value, length) => {
    if (!value) return null
    if (value.length > length) return `Must not exceed ${length} characters`
    return null
  },

  // Pattern validation
  pattern: (value, pattern, message) => {
    if (!value) return 'This field is required'
    if (!pattern.test(value)) return message || 'Invalid format'
    return null
  },
}

// Form validation function
export const validateForm = (formData, validationRules) => {
  const errors = {}

  Object.entries(validationRules).forEach(([fieldName, rules]) => {
    const value = formData[fieldName]

    for (const rule of rules) {
      const error = rule(value)
      if (error) {
        errors[fieldName] = error
        break
      }
    }
  })

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  }
}

// Field validation
export const validateField = (fieldName, value, rules) => {
  for (const rule of rules) {
    const error = rule(value)
    if (error) return error
  }
  return null
}
