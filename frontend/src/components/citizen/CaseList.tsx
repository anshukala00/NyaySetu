import { useState } from 'react'
import { Search, Filter, Loader } from 'lucide-react'
import { useCaseStore } from '../../store/caseStore'

type FilterStatus = 'all' | 'FILED' | 'IN_REVIEW' | 'HEARING_SCHEDULED'

export const CaseList = () => {
  const { cases, loading, error } = useCaseStore()
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState<FilterStatus>('all')
  const [selectedCase, setSelectedCase] = useState<any>(null)

  console.log('[CaseList] Render - cases:', cases.length, 'loading:', loading, 'error:', error)

  const filteredCases = cases.filter(caseItem => {
    const matchesSearch = caseItem.title.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = filterStatus === 'all' || caseItem.status === filterStatus
    return matchesSearch && matchesStatus
  })

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
      <h1 className="text-3xl font-bold text-gray-900 mb-2">My Cases</h1>
      <p className="text-gray-600 mb-8">View and manage all your filed cases</p>

      {/* Search and Filter */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div className="relative">
          <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search cases by title..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-gray-400" />
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value as FilterStatus)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Cases</option>
            <option value="FILED">Filed</option>
            <option value="IN_REVIEW">In Review</option>
            <option value="HEARING_SCHEDULED">Hearing Scheduled</option>
          </select>
        </div>
      </div>

      {/* Cases List */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
          <p className="text-red-800 font-medium">Error loading cases</p>
          <p className="text-red-600 text-sm mt-1">{error}</p>
        </div>
      )}
      
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader className="w-8 h-8 text-blue-600 animate-spin" />
        </div>
      ) : filteredCases.length > 0 ? (
        <div className="space-y-4">
          {filteredCases.map((caseItem) => (
            <div
              key={caseItem.id}
              onClick={() => setSelectedCase(selectedCase?.id === caseItem.id ? null : caseItem)}
              className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition cursor-pointer"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900">{caseItem.title}</h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Case ID: {caseItem.id}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(caseItem.status)}`}>
                    {caseItem.status}
                  </span>
                  {caseItem.priority && (
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(caseItem.priority)}`}>
                      {caseItem.priority}
                    </span>
                  )}
                </div>
              </div>

              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {caseItem.description}
              </p>

              {selectedCase?.id === caseItem.id && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h4 className="font-semibold text-gray-900 mb-2">Full Description:</h4>
                  <p className="text-gray-600 text-sm mb-4">{caseItem.description}</p>
                  
                  {caseItem.ai_summary && (
                    <>
                      <h4 className="font-semibold text-gray-900 mb-2">AI Summary:</h4>
                      <p className="text-gray-600 text-sm bg-blue-50 p-3 rounded">{caseItem.ai_summary}</p>
                    </>
                  )}
                </div>
              )}

              <div className="flex items-center justify-between text-sm text-gray-500">
                <span>Filed on {new Date(caseItem.created_at).toLocaleDateString()}</span>
                <div className="flex items-center gap-4">
                  {caseItem.ai_summary && (
                    <span className="text-blue-600 font-medium">AI Summary Available</span>
                  )}
                  <span className="text-blue-600 font-medium">
                    {selectedCase?.id === caseItem.id ? 'Click to collapse' : 'Click to expand'}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">
            {searchTerm || filterStatus !== 'all'
              ? 'No cases match your search or filter'
              : 'You haven\'t filed any cases yet'}
          </p>
          {!searchTerm && filterStatus === 'all' && (
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
              File Your First Case
            </button>
          )}
        </div>
      )}
    </div>
  )
}
