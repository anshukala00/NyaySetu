import { useCaseStore } from '../../store/caseStore'

export const Analytics = () => {
  const { cases } = useCaseStore()

  // Calculate statistics
  const totalCases = cases.length
  const casesByStatus = {
    FILED: cases.filter(c => c.status === 'FILED').length,
    IN_REVIEW: cases.filter(c => c.status === 'IN_REVIEW').length,
    HEARING_SCHEDULED: cases.filter(c => c.status === 'HEARING_SCHEDULED').length
  }

  const casesByPriority = {
    HIGH: cases.filter(c => c.priority === 'HIGH').length,
    REGULAR: cases.filter(c => c.priority === 'REGULAR').length
  }

  const avgResolutionTime = cases.length > 0
    ? Math.round(
        cases.reduce((sum, c) => {
          const created = new Date(c.created_at).getTime()
          const now = new Date().getTime()
          return sum + (now - created)
        }, 0) / cases.length / (1000 * 60 * 60 * 24)
      )
    : 0

  const statusPercentages = {
    FILED: totalCases > 0 ? Math.round((casesByStatus.FILED / totalCases) * 100) : 0,
    IN_REVIEW: totalCases > 0 ? Math.round((casesByStatus.IN_REVIEW / totalCases) * 100) : 0,
    HEARING_SCHEDULED: totalCases > 0 ? Math.round((casesByStatus.HEARING_SCHEDULED / totalCases) * 100) : 0
  }

  const priorityPercentages = {
    HIGH: totalCases > 0 ? Math.round((casesByPriority.HIGH / totalCases) * 100) : 0,
    REGULAR: totalCases > 0 ? Math.round((casesByPriority.REGULAR / totalCases) * 100) : 0
  }

  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg shadow-sm p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
        <p className="text-gray-600 mb-8">Case statistics and performance metrics</p>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6">
            <p className="text-gray-600 text-sm font-medium">Total Cases</p>
            <p className="text-3xl font-bold text-blue-600 mt-2">{totalCases}</p>
          </div>

          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg p-6">
            <p className="text-gray-600 text-sm font-medium">Avg Resolution Time</p>
            <p className="text-3xl font-bold text-yellow-600 mt-2">{avgResolutionTime} days</p>
          </div>

          <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-lg p-6">
            <p className="text-gray-600 text-sm font-medium">High Priority</p>
            <p className="text-3xl font-bold text-red-600 mt-2">{casesByPriority.HIGH}</p>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6">
            <p className="text-gray-600 text-sm font-medium">Completed</p>
            <p className="text-3xl font-bold text-green-600 mt-2">{casesByStatus.HEARING_SCHEDULED}</p>
          </div>
        </div>

        {/* Case Distribution by Status */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Case Distribution by Status</h3>
            <div className="space-y-4">
              {Object.entries(casesByStatus).map(([status, count]) => (
                <div key={status}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">{status}</span>
                    <span className="text-sm font-bold text-gray-900">{statusPercentages[status as keyof typeof statusPercentages]}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${
                        status === 'FILED' ? 'bg-blue-600' :
                        status === 'IN_REVIEW' ? 'bg-yellow-600' :
                        'bg-green-600'
                      }`}
                      style={{
                        width: `${statusPercentages[status as keyof typeof statusPercentages]}%`
                      }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">{count} cases</p>
                </div>
              ))}
            </div>
          </div>

          {/* Case Distribution by Priority */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Case Distribution by Priority</h3>
            <div className="space-y-4">
              {Object.entries(casesByPriority).map(([priority, count]) => (
                <div key={priority}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">{priority}</span>
                    <span className="text-sm font-bold text-gray-900">{priorityPercentages[priority as keyof typeof priorityPercentages]}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${
                        priority === 'HIGH' ? 'bg-red-600' : 'bg-gray-600'
                      }`}
                      style={{
                        width: `${priorityPercentages[priority as keyof typeof priorityPercentages]}%`
                      }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">{count} cases</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Summary Statistics */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-blue-900 mb-4">Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-blue-800">
            <div>
              <p className="font-semibold mb-1">Pending Cases</p>
              <p>{casesByStatus.FILED + casesByStatus.IN_REVIEW} cases awaiting action</p>
            </div>
            <div>
              <p className="font-semibold mb-1">High Priority Cases</p>
              <p>{casesByPriority.HIGH} cases require urgent attention</p>
            </div>
            <div>
              <p className="font-semibold mb-1">Completion Rate</p>
              <p>{totalCases > 0 ? Math.round((casesByStatus.HEARING_SCHEDULED / totalCases) * 100) : 0}% of cases completed</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
