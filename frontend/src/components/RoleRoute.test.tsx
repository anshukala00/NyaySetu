import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { RoleRoute } from './RoleRoute';

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

describe('RoleRoute', () => {
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

  it('should render children when user has allowed role', () => {
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
        <RoleRoute allowedRoles={['CITIZEN']}>
          <div>Citizen Content</div>
        </RoleRoute>
      </BrowserRouter>
    );

    expect(screen.getByText('Citizen Content')).toBeInTheDocument();
  });

  it('should redirect when user does not have allowed role', () => {
    render(
      <BrowserRouter>
        <RoleRoute allowedRoles={['JUDGE']}>
          <div>Judge Content</div>
        </RoleRoute>
      </BrowserRouter>
    );

    // Should not render judge content
    expect(screen.queryByText('Judge Content')).not.toBeInTheDocument();
  });

  it('should redirect to login when not authenticated', () => {
    render(
      <BrowserRouter>
        <RoleRoute allowedRoles={['CITIZEN']}>
          <div>Protected Content</div>
        </RoleRoute>
      </BrowserRouter>
    );

    // Should not render protected content
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });

  it('should allow multiple roles', () => {
    mockAuthState = {
      isAuthenticated: true,
      user: { id: 'user-123', email: 'test@example.com', role: 'JUDGE' as const },
      userId: 'user-123',
      userRole: 'JUDGE' as const,
      accessToken: 'test-token',
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      setAuth: vi.fn(),
      initializeAuth: vi.fn(),
    };

    render(
      <BrowserRouter>
        <RoleRoute allowedRoles={['CITIZEN', 'JUDGE']}>
          <div>Multi-Role Content</div>
        </RoleRoute>
      </BrowserRouter>
    );

    expect(screen.getByText('Multi-Role Content')).toBeInTheDocument();
  });
});
