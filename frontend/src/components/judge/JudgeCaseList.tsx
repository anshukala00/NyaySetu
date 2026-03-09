import { useState } from 'react'
import { Search, Filter, Loader, Zap } from 'lucide-react'
import { useCaseStore } from '../../store/caseStore'
import { caseService } from '../../services/api'

type FilterStatus = 'all' | 'FILED' | 'IN_REVIEW' | 'HEARING_SCHEDULED'
type FilterPriority = 'all' | 'HIGH' | 'REGULAR'

export const JudgeCaseList = () => {
  const { cases, loading, error, updateCase } = useCaseStore()
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState<FilterStatus>('all')
  const [filterPriority, setFilterPriority] = useState<FilterPriority>('all')
  const [sortBy, setSortBy] = useState<'date' | 'priority' | 'status'>('date')
  const [generatingSummary, setGeneratingSummary] = useState<string | null>(null)

  console.log('[JudgeCaseList] Render - cases:', cases.length, 'loading:', loading, 'error:', error)

  const filteredCases = cases
    .filter(caseItem => {
      const matchesSearch = 
        caseItem.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        caseItem.id.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesStatus = filterStatus === 'all' || caseItem.status === filterStatus
      const matchesPriority = filterPriority === 'all' || caseItem.priority === filterPriority
      return matchesSearch && matchesStatus && matchesPriority
    })
    .sort((a, b) => {
      if (sortBy === 'date') {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      } else if (sortBy === 'priority') {
        const priorityOrder = { HIGH: 0, REGULAR: 1 }
        return (priorityOrder[a.priority as keyof typeof priorityOrder] || 2) - 
               (priorityOrder[b.priority as keyof typeof priorityOrder] || 2)
      } else {
        const statusOrder = { FILED: 0, IN_REVIEW: 1, HEARING_SCHEDULED: 2 }
        return (statusOrder[a.status as keyof typeof statusOrder] || 3) - 
               (statusOrder[b.status as keyof typeof statusOrder] || 3)
      }
    })

  const handleGenerateSummary = async (caseId: string) => {
    setGeneratingSummary(caseId)
    try {
      const summary = await caseService.generateSummary(caseId)
      const updatedCase = cases.find(c => c.id === caseId)
      if (updatedCase) {
        updateCase({ ...updatedCase, ai_summary: summary })
      }
    } catch (error) {
      console.error('Failed to generate summary:', error)
    } finally {
      setGeneratingSummary(null)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'FILED':
        return 'bg-blue-100 text-blue-700'
      case 'IN_REVIEW':
        return 'bg-yellow-100 text-yellow-700'
      case 'HEARING_SCHEDULED':
        return 'bg-green-100 text-green-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  const getPriorityColor = (priority: string | null) => {
    if (!priority) return 'bg-gray-100 text-gray-700'
    return priority === 'HIGH' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">All Cases</h1>
      <p className="text-gray-600 mb-8">Review and manage all cases in the system</p>

      {/* Search and Filters */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="relative md:col-span-2">
          <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search by title or case ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>

        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value as FilterStatus)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        >
          <option value="all">All Status</option>
          <option value="FILED">Filed</option>
          <option value="IN_REVIEW">In Review</option>
          <option value="HEARING_SCHEDULED">Hearing Scheduled</option>
        </select>

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as any)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        >
          <option value="date">Sort by Date</option>
          <option value="priority">Sort by Priority</option>
          <option value="status">Sort by Status</option>
        </select>
      </div>

      {/* Cases Table */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
          <p className="text-red-800 font-medium">Error loading cases</p>
          <p className="text-red-600 text-sm mt-1">{error}</p>
        </div>
      )}
      
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader className="w-8 h-8 text-purple-600 animate-spin" />
        </div>
      ) : filteredCases.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Case ID</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Title</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Status</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Priority</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Filed Date</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredCases.map((caseItem) => (
                <tr key={caseItem.id} className="border-b border-gray-200 hover:bg-gray-50 transition">
                  <td className="py-4 px-4 text-sm text-gray-600 font-mono">{caseItem.id.slice(0, 8)}...</td>
                  <td className="py-4 px-4 text-sm font-medium text-gray-900">{caseItem.title}</td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(caseItem.status)}`}>
                      {caseItem.status}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    {caseItem.priority && (
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(caseItem.priority)}`}>
                        {caseItem.priority}
                      </span>
                    )}
                  </td>
                  <td className="py-4 px-4 text-sm text-gray-600">
                    {new Date(caseItem.created_at).toLocaleDateString()}
                  </td>
                  <td className="py-4 px-4">
                    <button
                      onClick={() => handleGenerateSummary(caseItem.id)}
                      disabled={generatingSummary === caseItem.id || !!caseItem.ai_summary}
                      className="flex items-center gap-1 px-3 py-1 text-sm bg-purple-100 text-purple-700 rounded hover:bg-purple-200 transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {generatingSummary === caseItem.id ? (
                        <Loader className="w-4 h-4 animate-spin" />
                      ) : (
                        <Zap className="w-4 h-4" />
                      )}
                      {caseItem.ai_summary ? 'Summary Done' : 'Generate'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-600">
            {searchTerm || filterStatus !== 'all'
              ? 'No cases match your search or filter'
              : 'No cases available'}
          </p>
        </div>
      )}
    </div>
  )
}
