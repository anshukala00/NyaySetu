import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Menu, X, LogOut, Home, FileText, List, HelpCircle } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { useCaseStore } from '../store/caseStore'
import { CitizenDashboard } from '../components/citizen/CitizenDashboard'
import { CaseForm } from '../components/citizen/CaseForm'
import { CaseList } from '../components/citizen/CaseList'

type Tab = 'dashboard' | 'file-case' | 'my-cases' | 'help'

export const CitizenPortal = () => {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<Tab>('dashboard')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { user, logout } = useAuthStore()
  const { fetchCases } = useCaseStore()

  useEffect(() => {
    console.log('CitizenPortal mounted, fetching cases...')
    fetchCases().catch(err => {
      console.error('Failed to fetch cases on mount:', err)
    })
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'file-case', label: 'File Case', icon: FileText },
    { id: 'my-cases', label: 'My Cases', icon: List },
    { id: 'help', label: 'Help', icon: HelpCircle }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold text-blue-600">Nyaysetu</span>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-8">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 font-semibold">
                    {user?.email?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-900">{user?.email}</div>
                  <div className="text-xs text-gray-500">Citizen</div>
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 transition"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 hover:bg-gray-100 rounded-lg transition"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className={`md:col-span-1 ${mobileMenuOpen ? 'block' : 'hidden md:block'}`}>
            <div className="bg-white rounded-lg shadow-sm p-4 space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActiveTab(item.id as Tab)
                      setMobileMenuOpen(false)
                    }}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                      activeTab === item.id
                        ? 'bg-blue-50 text-blue-600 font-semibold'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {item.label}
                  </button>
                )
              })}
              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition mt-4"
              >
                <LogOut className="w-5 h-5" />
                Logout
              </button>
            </div>
          </div>

          {/* Main Content */}
          <div className="md:col-span-3">
            {activeTab === 'dashboard' && <CitizenDashboard onNavigateToTab={setActiveTab} />}
            {activeTab === 'file-case' && <CaseForm />}
            {activeTab === 'my-cases' && <CaseList />}
            {activeTab === 'help' && (
              <div className="bg-white rounded-lg shadow-sm p-8 text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Help & Support</h2>
                <p className="text-gray-600 mb-6">
                  For assistance, please contact our support team at support@nyaysetu.com
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
