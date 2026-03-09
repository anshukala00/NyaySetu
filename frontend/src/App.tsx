import { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import { LandingPage } from './pages/LandingPage'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { CitizenPortal } from './pages/CitizenPortal'
import { JudgeDashboard } from './pages/JudgeDashboard'
import { ProtectedRoute } from './components/ProtectedRoute'
import { RoleRoute } from './components/RoleRoute'

function App() {
  const { initializeAuth } = useAuthStore()

  useEffect(() => {
    initializeAuth()
  }, [])

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        <Route
          path="/citizen-portal"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={['CITIZEN']}>
                <CitizenPortal />
              </RoleRoute>
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/judge-dashboard"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={['JUDGE']}>
                <JudgeDashboard />
              </RoleRoute>
            </ProtectedRoute>
          }
        />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
