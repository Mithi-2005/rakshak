// Format currency to INR
export const formatCurrency = (amount) => {
  if (!amount) return '₹0'
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
  }).format(amount)
}

// Format date
export const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

// Validate email
export const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// Validate phone
export const isValidPhone = (phone) => {
  const re = /^[0-9]{10}$/
  return re.test(phone.replace(/\D/g, ''))
}

// Format phone number
export const formatPhone = (phone) => {
  const cleaned = phone.replace(/\D/g, '')
  if (cleaned.length === 10) {
    return `${cleaned.slice(0, 5)} ${cleaned.slice(5)}`
  }
  return phone
}

// Get age from date of birth
export const calculateAge = (dob) => {
  const today = new Date()
  const birthDate = new Date(dob)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  return age
}

// Debounce function
export const debounce = (func, delay) => {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func(...args), delay)
  }
}

// Throttle function
export const throttle = (func, limit) => {
  let inThrottle
  return (...args) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// Get initials from name
export const getInitials = (name) => {
  if (!name) return ''
  return name
    .split(' ')
    .map(part => part.charAt(0).toUpperCase())
    .join('')
    .slice(0, 2)
}

// Truncate text
export const truncateText = (text, length) => {
  if (text.length <= length) return text
  return text.slice(0, length) + '...'
}

// Local storage manager
export const storage = {
  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error('Error saving to localStorage:', error)
    }
  },
  get: (key) => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : null
    } catch (error) {
      console.error('Error reading from localStorage:', error)
      return null
    }
  },
  remove: (key) => {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error('Error removing from localStorage:', error)
    }
  },
  clear: () => {
    try {
      localStorage.clear()
    } catch (error) {
      console.error('Error clearing localStorage:', error)
    }
  },
}

// Check if device is mobile
export const isMobile = () => {
  return window.innerWidth < 768
}

// Deep clone
export const deepClone = (obj) => {
  return JSON.parse(JSON.stringify(obj))
}

// Group array by key
export const groupBy = (array, key) => {
  return array.reduce((result, item) => {
    const group = item[key]
    if (!result[group]) result[group] = []
    result[group].push(item)
    return result
  }, {})
}
