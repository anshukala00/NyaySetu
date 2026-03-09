import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('user_role')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient


// Auth Service
export const authService = {
  register: async (email: string, password: string, role: string) => {
    const response = await apiClient.post('/auth/register', {
      email,
      password,
      role
    })
    return response.data
  },

  login: async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login', {
      email,
      password
    })
    return response.data
  }
}

// Case Service
export const caseService = {
  createCase: async (title: string, description: string) => {
    const response = await apiClient.post('/cases', {
      title,
      description
    })
    return response.data
  },

  getCases: async (page: number = 1, limit: number = 50) => {
    const response = await apiClient.get('/cases', {
      params: { page, limit }
    })
    return response.data
  },

  getCaseById: async (caseId: string) => {
    const response = await apiClient.get(`/cases/${caseId}`)
    return response.data
  },

  updateCaseStatus: async (caseId: string, status: string) => {
    const response = await apiClient.put(`/cases/${caseId}`, {
      status
    })
    return response.data
  },

  generateSummary: async (caseId: string) => {
    const response = await apiClient.post(`/ai/summarize/${caseId}`)
    return response.data.ai_summary
  }
}

// Precedent Service
export const precedentService = {
  search: async (query: string, limit: number = 5) => {
    const response = await apiClient.get('/precedents/search', {
      params: { q: query, limit }
    })
    return response.data.results
  }
}
