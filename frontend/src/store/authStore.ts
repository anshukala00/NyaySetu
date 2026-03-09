import { create } from 'zustand'
import apiClient from '../services/api'

interface User {
  email: string
  id: string
  role: 'CITIZEN' | 'JUDGE'
}

interface AuthState {
  isAuthenticated: boolean
  userId: string | null
  userRole: 'CITIZEN' | 'JUDGE' | null
  accessToken: string | null
  user: User | null
  isInitialized: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, role: 'CITIZEN' | 'JUDGE') => Promise<void>
  logout: () => void
  setAuth: (token: string, userId: string, role: 'CITIZEN' | 'JUDGE', email?: string) => void
  initializeAuth: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  userId: null,
  userRole: null,
  accessToken: null,
  user: null,
  isInitialized: false,

  login: async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/login', { email, password })
      const { access_token, user_id, role } = response.data

      localStorage.setItem('access_token', access_token)
      localStorage.setItem('user_id', user_id)
      localStorage.setItem('user_role', role)
      localStorage.setItem('user_email', email)

      set({
        isAuthenticated: true,
        accessToken: access_token,
        userId: user_id,
        userRole: role,
        user: { email, id: user_id, role },
        isInitialized: true
      })
    } catch (error) {
      throw error
    }
  },

  register: async (email: string, password: string, role: 'CITIZEN' | 'JUDGE') => {
    try {
      const response = await apiClient.post('/auth/register', { email, password, role })
      const { access_token, user_id } = response.data

      localStorage.setItem('access_token', access_token)
      localStorage.setItem('user_id', user_id)
      localStorage.setItem('user_role', role)
      localStorage.setItem('user_email', email)

      set({
        isAuthenticated: true,
        accessToken: access_token,
        userId: user_id,
        userRole: role,
        user: { email, id: user_id, role },
        isInitialized: true
      })
    } catch (error) {
      throw error
    }
  },

  setAuth: (token: string, userId: string, role: 'CITIZEN' | 'JUDGE', email?: string) => {
    localStorage.setItem('access_token', token)
    localStorage.setItem('user_id', userId)
    localStorage.setItem('user_role', role)
    if (email) {
      localStorage.setItem('user_email', email)
    }

    set({
      isAuthenticated: true,
      accessToken: token,
      userId,
      userRole: role,
      user: { email: email || '', id: userId, role },
      isInitialized: true
    })
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('user_role')
    localStorage.removeItem('user_email')

    set({
      isAuthenticated: false,
      accessToken: null,
      userId: null,
      userRole: null,
      user: null,
      isInitialized: true
    })
  },

  initializeAuth: () => {
    const token = localStorage.getItem('access_token')
    const userId = localStorage.getItem('user_id')
    const userRole = localStorage.getItem('user_role') as 'CITIZEN' | 'JUDGE' | null
    const email = localStorage.getItem('user_email')

    console.log('Initializing auth:', { token: token ? 'exists' : 'missing', userId, userRole, email })

    if (token && userId && userRole) {
      set({
        isAuthenticated: true,
        accessToken: token,
        userId,
        userRole,
        user: { email: email || '', id: userId, role: userRole },
        isInitialized: true
      })
      console.log('Auth initialized successfully')
    } else {
      set({ isInitialized: true })
      console.log('Auth initialization failed - missing credentials')
    }
  },
}))
