import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Menu, X, LogOut, Home, List, BookOpen, BarChart3 } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { useCaseStore } from '../store/caseStore'
import { JudgeDashboardOverview } from '../components/judge/JudgeDashboardOverview'
import { JudgeCaseList } from '../components/judge/JudgeCaseList'
import { PrecedentSearch } from '../components/judge/PrecedentSearch'
import { Analytics } from '../components/judge/Analytics'

type Tab = 'dashboard' | 'cases' | 'precedents' | 'analytics'

export const JudgeDashboard = () => {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<Tab>('dashboard')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { user, logout } = useAuthStore()
  const { fetchCases } = useCaseStore()

  useEffect(() => {
    console.log('JudgeDashboard mounted, fetching cases...')
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
    { id: 'cases', label: 'All Cases', icon: List },
    { id: 'precedents', label: 'Precedents', icon: BookOpen },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 }
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
                <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 font-semibold">
                    {user?.email?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-900">{user?.email}</div>
                  <div className="text-xs text-gray-500">Judge</div>
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
                        ? 'bg-purple-50 text-purple-600 font-semibold'
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
            {activeTab === 'dashboard' && <JudgeDashboardOverview />}
            {activeTab === 'cases' && <JudgeCaseList />}
            {activeTab === 'precedents' && <PrecedentSearch />}
            {activeTab === 'analytics' && <Analytics />}
          </div>
        </div>
      </div>
    </div>
  )
}
