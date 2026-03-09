import { create } from 'zustand'
import apiClient from '../services/api'

interface Case {
  id: string
  title: string
  description: string
  status: string
  user_id: string
  judge_id: string | null
  priority: string | null
  ai_summary: string | null
  created_at: string
  citizen?: { email: string }
}

interface CaseState {
  cases: Case[]
  currentCase: Case | null
  loading: boolean
  error: string | null
  fetchCases: () => Promise<void>
  fetchCaseById: (id: string) => Promise<void>
  createCase: (title: string, description: string) => Promise<void>
  addCase: (caseData: Case) => void
  updateCase: (caseData: Case) => void
  generateSummary: (caseId: string) => Promise<void>
  clearError: () => void
}

export const useCaseStore = create<CaseState>((set) => ({
  cases: [],
  currentCase: null,
  loading: false,
  error: null,

  fetchCases: async () => {
    set({ loading: true, error: null })
    try {
      console.log('[CaseStore] Fetching cases...')
      const response = await apiClient.get('/cases')
      console.log('[CaseStore] Response received:', response.status, response.data)
      
      // Backend returns { cases: [...], total, page, limit }
      const casesData = response.data.cases || response.data
      console.log('[CaseStore] Extracted cases:', casesData.length, 'cases')
      
      set({ cases: casesData, loading: false })
    } catch (error: any) {
      console.error('[CaseStore] Fetch cases error:', error)
      console.error('[CaseStore] Error response:', error.response?.data)
      console.error('[CaseStore] Error status:', error.response?.status)
      
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to fetch cases'
      set({ error: errorMessage, loading: false, cases: [] })
      // Don't throw - let the UI handle the error state
    }
  },

  fetchCaseById: async (id: string) => {
    set({ loading: true, error: null })
    try {
      const response = await apiClient.get(`/cases/${id}`)
      set({ currentCase: response.data, loading: false })
    } catch (error: any) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  createCase: async (title: string, description: string) => {
    set({ loading: true, error: null })
    try {
      const response = await apiClient.post('/cases', { title, description })
      set((state) => ({
        cases: [...state.cases, response.data],
        loading: false,
      }))
    } catch (error: any) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  addCase: (caseData: Case) => {
    set((state) => ({
      cases: [...state.cases, caseData]
    }))
  },

  updateCase: (caseData: Case) => {
    set((state) => ({
      cases: state.cases.map(c => c.id === caseData.id ? caseData : c),
      currentCase: state.currentCase?.id === caseData.id ? caseData : state.currentCase
    }))
  },

  generateSummary: async (caseId: string) => {
    set({ loading: true, error: null })
    try {
      const response = await apiClient.post(`/ai/summarize/${caseId}`)
      set((state) => ({
        currentCase: state.currentCase
          ? { ...state.currentCase, ai_summary: response.data.summary }
          : null,
        loading: false,
      }))
    } catch (error: any) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  clearError: () => {
    set({ error: null })
  },
}))
