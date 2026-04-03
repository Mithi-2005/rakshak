import { useState, useCallback } from 'react'

export function useApi(apiFunction) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const execute = useCallback(async (...args) => {
    setLoading(true)
    setError(null)
    try {
      const result = await apiFunction(...args)
      setData(result)
      return result
    } catch (err) {
      setError(err.response?.data?.message || err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [apiFunction])

  return { data, loading, error, execute }
}

export function useAsync(asyncFunction, immediate = true) {
  const [status, setStatus] = useState('idle')
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const execute = useCallback(async (...args) => {
    setStatus('pending')
    setData(null)
    setError(null)
    try {
      const result = await asyncFunction(...args)
      setData(result)
      setStatus('success')
      return result
    } catch (error) {
      setError(error)
      setStatus('error')
      throw error
    }
  }, [asyncFunction])

  return { execute, status, data, error }
}
