import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useAuthStore } from './authStore';

// Mock the API client
vi.mock('../services/api', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  },
}));

describe('Auth Store', () => {
  beforeEach(() => {
    localStorage.clear();
    useAuthStore.setState({
      isAuthenticated: false,
      userId: null,
      userRole: null,
      accessToken: null,
      user: null,
    });
  });

  it('should initialize with default state', () => {
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.accessToken).toBeNull();
    expect(state.isAuthenticated).toBe(false);
  });

  it('should logout user', () => {
    useAuthStore.setState({
      user: { id: 'user-123', email: 'test@example.com', role: 'CITIZEN' },
      accessToken: 'test-token',
      isAuthenticated: true,
      userId: 'user-123',
      userRole: 'CITIZEN',
    });

    localStorage.setItem('access_token', 'test-token');

    const store = useAuthStore.getState();
    store.logout();

    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.accessToken).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(localStorage.getItem('access_token')).toBeNull();
  });

  it('should restore session from localStorage', () => {
    localStorage.setItem('access_token', 'test-token');
    localStorage.setItem('user_id', 'user-123');
    localStorage.setItem('user_role', 'CITIZEN');
    localStorage.setItem('user_email', 'test@example.com');

    const store = useAuthStore.getState();
    store.initializeAuth();

    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(true);
    expect(state.accessToken).toBe('test-token');
    expect(state.userId).toBe('user-123');
    expect(state.userRole).toBe('CITIZEN');
    expect(state.user?.id).toBe('user-123');
  });

  it('should set auth with setAuth method', () => {
    const store = useAuthStore.getState();
    store.setAuth('test-token', 'user-123', 'CITIZEN', 'test@example.com');

    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(true);
    expect(state.accessToken).toBe('test-token');
    expect(state.userId).toBe('user-123');
    expect(state.userRole).toBe('CITIZEN');
    expect(state.user?.email).toBe('test@example.com');
    expect(localStorage.getItem('access_token')).toBe('test-token');
  });

  it('should handle logout and clear localStorage', () => {
    localStorage.setItem('access_token', 'test-token');
    localStorage.setItem('user_id', 'user-123');
    localStorage.setItem('user_role', 'CITIZEN');
    localStorage.setItem('user_email', 'test@example.com');

    const store = useAuthStore.getState();
    store.logout();

    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('user_id')).toBeNull();
    expect(localStorage.getItem('user_role')).toBeNull();
    expect(localStorage.getItem('user_email')).toBeNull();
  });
});
