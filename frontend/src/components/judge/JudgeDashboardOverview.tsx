import { useEffect, useState } from 'react'
import { FileText, Clock, CheckCircle, ArrowRight } from 'lucide-react'
import { useCaseStore } from '../../store/caseStore'

interface CaseStats {
  total: number
  pending: number
  completed: number
}

export const JudgeDashboardOverview = () => {
  const [stats, setStats] = useState<CaseStats>({ total: 0, pending: 0, completed: 0 })
  const { cases } = useCaseStore()

  useEffect(() => {
    const total = cases.length
    const pending = cases.filter(c => c.status === 'FILED' || c.status === 'IN_REVIEW').length
    const completed = cases.filter(c => c.status === 'HEARING_SCHEDULED').length
    setStats({ total, pending, completed })
  }, [cases])

  const recentCases = cases.slice(0, 5)

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-purple-600 to-purple-700 rounded-lg shadow-lg p-8 text-white">
        <h1 className="text-3xl font-bold mb-2">Judge Dashboard</h1>
        <p className="text-purple-100">Review cases, generate summaries, and search precedents</p>
      </div>

      {/* Key Metrics */}
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
              <p className="text-gray-600 text-sm font-medium">Pending Review</p>
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
              <p className="text-gray-600 text-sm font-medium">Completed</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.completed}</p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <button className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition text-left">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">View All Cases</h3>
              <p className="text-gray-600 text-sm mt-1">Review and manage cases</p>
            </div>
            <ArrowRight className="w-5 h-5 text-purple-600" />
          </div>
        </button>

        <button className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition text-left">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Search Precedents</h3>
              <p className="text-gray-600 text-sm mt-1">Find relevant legal precedents</p>
            </div>
            <ArrowRight className="w-5 h-5 text-purple-600" />
          </div>
        </button>
      </div>

      {/* Recent Cases */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Recent Cases</h2>
        {recentCases.length > 0 ? (
          <div className="space-y-4">
            {recentCases.map((caseItem) => (
              <div
                key={caseItem.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition cursor-pointer"
              >
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{caseItem.title}</h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Filed by {caseItem.citizen?.email || 'Unknown'} on {new Date(caseItem.created_at).toLocaleDateString()}
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
            <p className="text-gray-600">No cases available</p>
          </div>
        )}
      </div>
    </div>
  )
}
