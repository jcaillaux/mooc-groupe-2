import axios from 'axios'

// Create a custom axios instance
const apiClient = axios.create({
  baseURL: '', // Your API base URL
  timeout: 10000,
})

// Function to set auth token
export const setAuthToken = (token) => {
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete apiClient.defaults.headers.common['Authorization']
  }
}

// Request interceptor (always gets the latest token)
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage on every request
    const token = localStorage.getItem('token')
    console.log(token)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for handling auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      // Token is invalid/expired
      localStorage.removeItem('token')
      window.location.href = '/landing-page' // Force redirect
    }
    return Promise.reject(error)
  }
)

export default apiClient