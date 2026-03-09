import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Search, Loader, AlertCircle } from 'lucide-react'
import { precedentService } from '../../services/api'

interface SearchFormData {
  query: string
  caseType?: string
  relevanceThreshold?: number
}

interface PrecedentResult {
  id: string
  title: string
  summary: string
  relevance_score: number
}

export const PrecedentSearch = () => {
  const { register, handleSubmit, watch } = useForm<SearchFormData>()
  const [results, setResults] = useState<PrecedentResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searched, setSearched] = useState(false)
  const [sortBy, setSortBy] = useState<'relevance' | 'name' | 'date'>('relevance')

  const onSubmit = async (data: SearchFormData) => {
    if (!data.query.trim()) {
      setError('Please enter a search query')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await precedentService.search(data.query)
      setResults(response)
      setSearched(true)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Search failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const sortedResults = [...results].sort((a, b) => {
    if (sortBy === 'relevance') {
      return b.relevance_score - a.relevance_score
    } else if (sortBy === 'name') {
      return a.title.localeCompare(b.title)
    }
    return 0
  })

  return (
    <div className="bg-white rounded-lg shadow-sm p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Precedent Search</h1>
      <p className="text-gray-600 mb-8">Find relevant legal precedents using semantic search</p>

      {/* Search Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="mb-8 space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search Query <span className="text-red-600">*</span>
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
            <input
              type="text"
              {...register('query', { required: 'Search query is required' })}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="e.g., property boundary dispute, contract breach..."
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Case Type (Optional)
            </label>
            <select
              {...register('caseType')}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">All Types</option>
              <option value="civil">Civil</option>
              <option value="criminal">Criminal</option>
              <option value="family">Family</option>
              <option value="property">Property</option>
              <option value="commercial">Commercial</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Relevance Threshold (Optional)
            </label>
            <input
              type="number"
              {...register('relevanceThreshold')}
              min="0"
              max="100"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="0-100"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading && <Loader className="w-4 h-4 animate-spin" />}
          {loading ? 'Searching...' : 'Search Precedents'}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Results */}
      {searched && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">
              Results ({sortedResults.length})
            </h2>
            {sortedResults.length > 0 && (
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="relevance">Sort by Relevance</option>
                <option value="name">Sort by Name</option>
              </select>
            )}
          </div>

          {sortedResults.length > 0 ? (
            <div className="space-y-4">
              {sortedResults.map((result, index) => (
                <div
                  key={index}
                  className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition cursor-pointer"
                >
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-lg font-semibold text-gray-900">{result.title}</h3>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-gray-600">Relevance:</span>
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full font-semibold">
                        {result.relevance_score}/5
                      </span>
                    </div>
                  </div>
                  <p className="text-gray-600 line-clamp-3">{result.summary}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-600">No precedents found matching your search</p>
            </div>
          )}
        </div>
      )}

      {/* Info Box */}
      {!searched && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="font-semibold text-blue-900 mb-2">How to search:</h3>
          <ul className="text-blue-800 text-sm space-y-1">
            <li>• Enter keywords related to your case</li>
            <li>• Optionally filter by case type</li>
            <li>• Results are ranked by relevance score</li>
            <li>• Click on any result to view full details</li>
          </ul>
        </div>
      )}
    </div>
  )
}
