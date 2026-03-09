import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Mic, AlertCircle, CheckCircle, Loader } from 'lucide-react'
import { caseService } from '../../services/api'
import { useCaseStore } from '../../store/caseStore'

interface CaseFormData {
  title: string
  description: string
  category?: string
}

export const CaseForm = () => {
  const { register, handleSubmit, watch, reset, formState: { errors } } = useForm<CaseFormData>()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [successCaseId, setSuccessCaseId] = useState<string | null>(null)
  const { addCase } = useCaseStore()

  const title = watch('title', '')
  const description = watch('description', '')

  const onSubmit = async (data: CaseFormData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await caseService.createCase(data.title, data.description)
      addCase(response)
      setSuccess(true)
      setSuccessCaseId(response.id)
      reset()
      setTimeout(() => setSuccess(false), 5000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to file case. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">File a New Case</h1>
      <p className="text-gray-600 mb-8">Provide details about your case for AI-powered triage and routing</p>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {success && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex gap-3">
          <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-green-700 font-semibold">Case filed successfully!</p>
            <p className="text-green-600 text-sm">Case ID: {successCaseId}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Case Title */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Case Title <span className="text-red-600">*</span>
          </label>
          <div className="relative">
            <input
              type="text"
              {...register('title', {
                required: 'Case title is required',
                maxLength: {
                  value: 200,
                  message: 'Title must be 200 characters or less'
                }
              })}
              maxLength={200}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter case title"
            />
            <div className="absolute right-3 top-2 text-sm text-gray-500">
              {title.length}/200
            </div>
          </div>
          {errors.title && (
            <p className="text-red-600 text-sm mt-1">{errors.title.message}</p>
          )}
        </div>

        {/* Case Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Case Description <span className="text-red-600">*</span>
          </label>
          <div className="relative">
            <textarea
              {...register('description', {
                required: 'Case description is required',
                maxLength: {
                  value: 10000,
                  message: 'Description must be 10,000 characters or less'
                }
              })}
              maxLength={10000}
              rows={8}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              placeholder="Describe your case in detail..."
            />
            <div className="absolute right-3 bottom-3 text-sm text-gray-500">
              {description.length}/10,000
            </div>
          </div>
          {errors.description && (
            <p className="text-red-600 text-sm mt-1">{errors.description.message}</p>
          )}
        </div>

        {/* Voice Input Button */}
        <div>
          <button
            type="button"
            className="flex items-center gap-2 px-4 py-2 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-medium group"
            title="Voice-to-text feature coming soon"
          >
            <Mic className="w-5 h-5 group-hover:text-blue-600 transition" />
            Add via Voice (Coming Soon)
          </button>
        </div>

        {/* Category Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Case Category (Optional)
          </label>
          <select
            {...register('category')}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Select a category</option>
            <option value="civil">Civil</option>
            <option value="criminal">Criminal</option>
            <option value="family">Family</option>
            <option value="property">Property</option>
            <option value="commercial">Commercial</option>
            <option value="other">Other</option>
          </select>
        </div>

        {/* Submit Button */}
        <div className="flex gap-4 pt-6">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading && <Loader className="w-4 h-4 animate-spin" />}
            {loading ? 'Filing Case...' : 'File Case'}
          </button>
          <button
            type="button"
            onClick={() => reset()}
            className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-semibold"
          >
            Clear
          </button>
        </div>
      </form>

      {/* Info Box */}
      <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">What happens next?</h3>
        <ul className="text-blue-800 text-sm space-y-1">
          <li>✓ Your case will be analyzed by our AI triage system</li>
          <li>✓ Priority will be assigned based on urgency</li>
          <li>✓ You'll receive updates as your case progresses</li>
          <li>✓ AI-generated summaries will be available for review</li>
        </ul>
      </div>
    </div>
  )
}
