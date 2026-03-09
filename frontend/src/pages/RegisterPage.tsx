import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { Scale, AlertCircle, CheckCircle, Loader, ChevronRight, ChevronLeft } from 'lucide-react'
import { authService } from '../services/api'

interface RegisterFormData {
  email: string
  password: string
  confirmPassword: string
  role: 'CITIZEN' | 'JUDGE'
}

export const RegisterPage = () => {
  const navigate = useNavigate()
  const { register, handleSubmit, watch, formState: { errors } } = useForm<RegisterFormData>({
    mode: 'onSubmit',
    defaultValues: { role: 'CITIZEN' }
  })
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const password = watch('password')
  const role = watch('role')

  const onSubmit = async (data: RegisterFormData) => {
    if (step === 1) {
      setStep(2)
      return
    }

    setLoading(true)
    setError(null)
    try {
      await authService.register(data.email, data.password, data.role)
      setSuccess(true)
      setTimeout(() => {
        navigate('/login')
      }, 2000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const roleDescriptions = {
    CITIZEN: {
      title: 'Citizen',
      description: 'File cases, track status, and view AI-generated summaries',
      icon: '👤'
    },
    JUDGE: {
      title: 'Judge',
      description: 'Review cases, generate summaries, and access analytics',
      icon: '⚖️'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Scale className="w-8 h-8 text-blue-600" />
            <span className="text-3xl font-bold text-gray-900">Nyaysetu</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Create Account</h1>
          <p className="text-gray-600 mt-2">Step {step} of 2</p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {success && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <p className="text-green-700 text-sm">Registration successful! Redirecting to login...</p>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {step === 1 ? (
              <>
                {/* Email Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="text"
                    {...register('email', {
                      required: 'Email is required',
                      pattern: {
                        value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                        message: 'Invalid email address'
                      }
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="you@example.com"
                  />
                  {errors.email && (
                    <p className="text-red-600 text-sm mt-1">{errors.email.message}</p>
                  )}
                </div>

                {/* Password Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Password
                  </label>
                  <input
                    type="password"
                    {...register('password', {
                      required: 'Password is required',
                      minLength: {
                        value: 8,
                        message: 'Password must be at least 8 characters'
                      }
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="••••••••"
                  />
                  {errors.password && (
                    <p className="text-red-600 text-sm mt-1">{errors.password.message}</p>
                  )}
                </div>

                {/* Confirm Password Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    {...register('confirmPassword', {
                      required: 'Please confirm your password',
                      validate: (value) => value === password || 'Passwords do not match'
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="••••••••"
                  />
                  {errors.confirmPassword && (
                    <p className="text-red-600 text-sm mt-1">{errors.confirmPassword.message}</p>
                  )}
                </div>
              </>
            ) : (
              <>
                {/* Role Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-4">
                    Select Your Role
                  </label>
                  <div className="space-y-3">
                    {(['CITIZEN', 'JUDGE'] as const).map((r) => (
                      <label key={r} className="flex items-center p-4 border-2 rounded-lg cursor-pointer transition"
                        style={{
                          borderColor: role === r ? '#2563eb' : '#e5e7eb',
                          backgroundColor: role === r ? '#eff6ff' : 'white'
                        }}
                      >
                        <input
                          type="radio"
                          value={r}
                          {...register('role')}
                          className="w-4 h-4 text-blue-600"
                        />
                        <div className="ml-4 flex-1">
                          <div className="font-semibold text-gray-900">
                            {roleDescriptions[r].icon} {roleDescriptions[r].title}
                          </div>
                          <div className="text-sm text-gray-600">
                            {roleDescriptions[r].description}
                          </div>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>
              </>
            )}

            {/* Navigation Buttons */}
            <div className="flex gap-3 pt-4">
              {step === 2 && (
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="flex-1 px-4 py-2 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-semibold flex items-center justify-center gap-2"
                >
                  <ChevronLeft className="w-4 h-4" />
                  Back
                </button>
              )}
              <button
                type="submit"
                disabled={loading}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading && <Loader className="w-4 h-4 animate-spin" />}
                {step === 1 ? (
                  <>
                    Next <ChevronRight className="w-4 h-4" />
                  </>
                ) : (
                  'Create Account'
                )}
              </button>
            </div>
          </form>

          {/* Login Link */}
          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="text-blue-600 hover:text-blue-700 font-semibold transition">
                Sign in here
              </Link>
            </p>
          </div>
        </div>

        {/* Back to Home */}
        <div className="text-center mt-6">
          <Link to="/" className="text-gray-600 hover:text-gray-900 transition">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  )
}
