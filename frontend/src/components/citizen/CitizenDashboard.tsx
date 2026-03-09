import { useEffect, useState } from 'react'
import { FileText, Clock, CheckCircle, ArrowRight } from 'lucide-react'
import { useCaseStore } from '../../store/caseStore'

interface CaseStats {
  total: number
  pending: number
  resolved: number
}

interface CitizenDashboardProps {
  onNavigateToTab?: (tab: 'file-case' | 'my-cases') => void
}

export const CitizenDashboard = ({ onNavigateToTab }: CitizenDashboardProps) => {
  const [stats, setStats] = useState<CaseStats>({ total: 0, pending: 0, resolved: 0 })
  const [loading, setLoading] = useState(true)
  const { cases } = useCaseStore()

  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true)
        // Calculate stats from cases
        const total = cases.length
        const pending = cases.filter(c => c.status === 'FILED' || c.status === 'IN_REVIEW').length
        const resolved = cases.filter(c => c.status === 'HEARING_SCHEDULED').length
        setStats({ total, pending, resolved })
      } catch (error) {
        console.error('Failed to load stats:', error)
      } finally {
        setLoading(false)
      }
    }

    loadStats()
  }, [cases])

  const recentCases = cases.slice(0, 5)

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg shadow-lg p-8 text-white">
        <h1 className="text-3xl font-bold mb-2">Welcome to Your Dashboard</h1>
        <p className="text-blue-100">Manage your cases and track their progress</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Total Cases</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.total}</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Pending Cases</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.pending}</p>
            </div>
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <Clock className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Resolved Cases</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.resolved}</p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <button
          onClick={() => onNavigateToTab?.('file-case')}
          className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition text-left"
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">File New Case</h3>
              <p className="text-gray-600 text-sm mt-1">Start a new case filing</p>
            </div>
            <ArrowRight className="w-5 h-5 text-blue-600" />
          </div>
        </button>

        <button
          onClick={() => onNavigateToTab?.('my-cases')}
          className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition text-left"
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">View My Cases</h3>
              <p className="text-gray-600 text-sm mt-1">See all your filed cases</p>
            </div>
            <ArrowRight className="w-5 h-5 text-blue-600" />
          </div>
        </button>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Recent Cases</h2>
        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-16 bg-gray-100 rounded-lg animate-pulse"></div>
            ))}
          </div>
        ) : recentCases.length > 0 ? (
          <div className="space-y-4">
            {recentCases.map((caseItem) => (
              <div
                key={caseItem.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition cursor-pointer"
              >
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{caseItem.title}</h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Filed on {new Date(caseItem.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    caseItem.status === 'FILED' ? 'bg-blue-100 text-blue-700' :
                    caseItem.status === 'IN_REVIEW' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {caseItem.status}
                  </span>
                  {caseItem.priority && (
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      caseItem.priority === 'HIGH' ? 'bg-red-100 text-red-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {caseItem.priority}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-600 mb-4">No cases filed yet</p>
            <button
              onClick={() => onNavigateToTab?.('file-case')}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              File Your First Case
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
