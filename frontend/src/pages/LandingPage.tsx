import { useNavigate } from 'react-router-dom'
import { Scale, Zap, BookOpen, Clock, Route as RouteIcon, ArrowRight } from 'lucide-react'

export const LandingPage = () => {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation Header */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <Scale className="w-8 h-8 text-blue-600" />
              <span className="text-2xl font-bold text-gray-900">Nyaysetu</span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition">Features</a>
              <a href="#portals" className="text-gray-600 hover:text-gray-900 transition">Portals</a>
              <a href="#impact" className="text-gray-600 hover:text-gray-900 transition">Impact</a>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/login')}
                className="px-4 py-2 text-blue-600 hover:text-blue-700 font-medium transition"
              >
                Login
              </button>
              <button
                onClick={() => navigate('/register')}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                Justice Fast, Fair, and for Everyone
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Streamline case management with AI-powered triage, real-time tracking, and intelligent precedent search.
              </p>
              <div className="flex gap-4">
                <button
                  onClick={() => navigate('/register')}
                  className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold flex items-center gap-2"
                >
                  Explore Portal <ArrowRight className="w-5 h-5" />
                </button>
                <button
                  className="px-8 py-3 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition font-semibold"
                >
                  View Demo
                </button>
              </div>
            </div>
            <div className="flex justify-center">
              <div className="w-64 h-64 bg-blue-600 rounded-full flex items-center justify-center shadow-2xl">
                <Scale className="w-32 h-32 text-white" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Unified Portals Section */}
      <section id="portals" className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">Unified Portals</h2>
          <p className="text-center text-gray-600 mb-12 text-lg">
            Tailored experiences for every role in the justice system
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Citizens Card */}
            <div className="bg-white border-2 border-gray-200 rounded-xl p-8 hover:shadow-lg hover:border-blue-300 transition">
              <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                <Scale className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Citizens</h3>
              <ul className="text-gray-600 space-y-2 mb-6">
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
                  File cases easily
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
                  Track case status
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
                  View AI summaries
                </li>
              </ul>
              <button
                onClick={() => navigate('/register')}
                className="w-full px-4 py-2 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition font-semibold"
              >
                Enter Portal
              </button>
            </div>

            {/* Advocates Card */}
            <div className="bg-white border-2 border-gray-200 rounded-xl p-8 hover:shadow-lg hover:border-blue-300 transition">
              <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                <BookOpen className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Advocates</h3>
              <ul className="text-gray-600 space-y-2 mb-6">
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-600 rounded-full"></span>
                  Manage cases
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-600 rounded-full"></span>
                  Search precedents
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-600 rounded-full"></span>
                  Collaborate
                </li>
              </ul>
              <button
                onClick={() => navigate('/register')}
                className="w-full px-4 py-2 border-2 border-green-600 text-green-600 rounded-lg hover:bg-green-50 transition font-semibold"
              >
                Enter Portal
              </button>
            </div>

            {/* Judges Card */}
            <div className="bg-white border-2 border-gray-200 rounded-xl p-8 hover:shadow-lg hover:border-blue-300 transition">
              <div className="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                <Zap className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Judges</h3>
              <ul className="text-gray-600 space-y-2 mb-6">
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-purple-600 rounded-full"></span>
                  Review cases
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-purple-600 rounded-full"></span>
                  Generate summaries
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-purple-600 rounded-full"></span>
                  Access analytics
                </li>
              </ul>
              <button
                onClick={() => navigate('/register')}
                className="w-full px-4 py-2 border-2 border-purple-600 text-purple-600 rounded-lg hover:bg-purple-50 transition font-semibold"
              >
                Enter Portal
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Key Features Section */}
      <section id="features" className="py-20 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">Key Features</h2>
          <p className="text-center text-gray-600 mb-12 text-lg">
            Powerful tools to transform the justice system
          </p>
          <div className="grid md:grid-cols-4 gap-8">
            {/* AI Triage */}
            <div className="bg-white rounded-xl p-8 text-center hover:shadow-lg transition">
              <div className="w-16 h-16 bg-yellow-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Zap className="w-8 h-8 text-yellow-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">AI-Powered Triage</h3>
              <p className="text-gray-600">
                Automatically prioritize cases based on urgency and complexity
              </p>
            </div>

            {/* Precedent Search */}
            <div className="bg-white rounded-xl p-8 text-center hover:shadow-lg transition">
              <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <BookOpen className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Precedent Search</h3>
              <p className="text-gray-600">
                Find relevant legal precedents instantly with semantic search
              </p>
            </div>

            {/* Real-Time Tracking */}
            <div className="bg-white rounded-xl p-8 text-center hover:shadow-lg transition">
              <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Clock className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Real-Time Tracking</h3>
              <p className="text-gray-600">
                Monitor case progress with live status updates
              </p>
            </div>

            {/* Smart Routing */}
            <div className="bg-white rounded-xl p-8 text-center hover:shadow-lg transition">
              <div className="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <RouteIcon className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Smart Case Routing</h3>
              <p className="text-gray-600">
                Intelligent assignment based on expertise and workload
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="impact" className="py-20 px-4 bg-gradient-to-r from-orange-500 to-orange-600">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-4">Join the Mission</h2>
          <p className="text-xl text-orange-100 mb-8 max-w-2xl mx-auto">
            Transform the justice system with technology that makes legal processes faster, fairer, and more accessible to everyone.
          </p>
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white bg-opacity-10 rounded-lg p-6 text-white">
              <div className="text-3xl font-bold mb-2">5 Crore+</div>
              <div className="text-orange-100">Cases Processed</div>
            </div>
            <div className="bg-white bg-opacity-10 rounded-lg p-6 text-white">
              <div className="text-3xl font-bold mb-2">98%</div>
              <div className="text-orange-100">Accuracy Rate</div>
            </div>
            <div className="bg-white bg-opacity-10 rounded-lg p-6 text-white">
              <div className="text-3xl font-bold mb-2">24/7</div>
              <div className="text-orange-100">Support Available</div>
            </div>
          </div>
          <button
            onClick={() => navigate('/register')}
            className="px-8 py-3 bg-white text-orange-600 rounded-lg hover:bg-orange-50 transition font-semibold text-lg"
          >
            Join the Mission
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            {/* Platform */}
            <div>
              <h4 className="text-white font-bold mb-4">Platform</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white transition">Features</a></li>
                <li><a href="#" className="hover:text-white transition">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition">Security</a></li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 className="text-white font-bold mb-4">Resources</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white transition">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                <li><a href="#" className="hover:text-white transition">Support</a></li>
              </ul>
            </div>

            {/* Stay Updated */}
            <div>
              <h4 className="text-white font-bold mb-4">Stay Updated</h4>
              <div className="flex gap-2">
                <input
                  type="email"
                  placeholder="Your email"
                  className="flex-1 px-4 py-2 rounded bg-gray-800 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
                <button className="px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 transition">
                  Subscribe
                </button>
              </div>
            </div>

            {/* Social */}
            <div>
              <h4 className="text-white font-bold mb-4">Follow Us</h4>
              <div className="flex gap-4">
                <a href="#" className="hover:text-white transition">Twitter</a>
                <a href="#" className="hover:text-white transition">LinkedIn</a>
                <a href="#" className="hover:text-white transition">GitHub</a>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8">
            <div className="flex justify-between items-center">
              <p>&copy; 2024 Nyaysetu. All rights reserved.</p>
              <div className="flex gap-6">
                <a href="#" className="hover:text-white transition">Privacy Policy</a>
                <a href="#" className="hover:text-white transition">Terms of Service</a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
