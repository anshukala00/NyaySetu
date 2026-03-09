import '@testing-library/jest-dom'
import { expect, afterEach, vi, beforeEach } from 'vitest'
import { cleanup } from '@testing-library/react'

// Suppress React Router v7 future flag warnings
const originalWarn = console.warn
console.warn = (...args: any[]) => {
  if (
    typeof args[0] === 'string' &&
    (args[0].includes('future') || args[0].includes('React Router'))
  ) {
    return
  }
  originalWarn(...args)
}

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock localStorage with proper implementation
const localStorageMock = (() => {
  let store: Record<string, string> = {}

  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString()
    },
    removeItem: (key: string) => {
      delete store[key]
    },
    clear: () => {
      store = {}
    },
  }
})()

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
})

// Mock window.location.href
delete (window as any).location
window.location = { href: '' } as any

// Mock lucide-react icons
vi.mock('lucide-react', () => ({
  Scale: () => null,
  AlertCircle: () => null,
  Loader: () => null,
  Menu: () => null,
  X: () => null,
  LogOut: () => null,
  Plus: () => null,
  Search: () => null,
  Filter: () => null,
  ChevronRight: () => null,
  ChevronLeft: () => null,
  Clock: () => null,
  CheckCircle: () => null,
  AlertTriangle: () => null,
  FileText: () => null,
  Briefcase: () => null,
  BarChart3: () => null,
  BookOpen: () => null,
  Mic: () => null,
  Send: () => null,
  ArrowLeft: () => null,
  Printer: () => null,
  TrendingUp: () => null,
  Users: () => null,
  Calendar: () => null,
  Home: () => null,
  Settings: () => null,
  HelpCircle: () => null,
}))
