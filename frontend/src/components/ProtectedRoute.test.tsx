import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ProtectedRoute } from './ProtectedRoute';

// Mock the auth store
let mockAuthState = {
  isAuthenticated: false,
  user: null,
  userId: null,
  userRole: null,
  accessToken: null,
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
  setAuth: vi.fn(),
  initializeAuth: vi.fn(),
};

vi.mock('../store/authStore', () => ({
  useAuthStore: vi.fn((selector: any) => {
    if (typeof selector === 'function') {
      return selector(mockAuthState);
    }
    return mockAuthState;
  }),
}));

describe('ProtectedRoute', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset mock auth state
    mockAuthState = {
      isAuthenticated: false,
      user: null,
      userId: null,
      userRole: null,
      accessToken: null,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      setAuth: vi.fn(),
      initializeAuth: vi.fn(),
    };
  });

  it('should render children when authenticated', () => {
    mockAuthState = {
      isAuthenticated: true,
      user: { id: 'user-123', email: 'test@example.com', role: 'CITIZEN' as const },
      userId: 'user-123',
      userRole: 'CITIZEN' as const,
      accessToken: 'test-token',
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      setAuth: vi.fn(),
      initializeAuth: vi.fn(),
    };

    render(
      <BrowserRouter>
        <ProtectedRoute>
          <div>Protected Content</div>
        </ProtectedRoute>
      </BrowserRouter>
    );

    expect(screen.getByText('Protected Content')).toBeInTheDocument();
  });

  it('should redirect to login when not authenticated', () => {
    render(
      <BrowserRouter>
        <ProtectedRoute>
          <div>Protected Content</div>
        </ProtectedRoute>
      </BrowserRouter>
    );

    // Should not render protected content
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });
});
