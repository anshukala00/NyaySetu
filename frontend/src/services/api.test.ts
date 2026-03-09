import { describe, it, expect, beforeEach, vi } from 'vitest';

// Hoist mock functions to ensure they're available during module initialization
const { mockPost, mockGet, mockPut } = vi.hoisted(() => ({
  mockPost: vi.fn(),
  mockGet: vi.fn(),
  mockPut: vi.fn(),
}));

// Mock axios before importing the API module
vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      post: mockPost,
      get: mockGet,
      put: mockPut,
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() },
      },
    })),
  },
}));

// Import after mocking
import { authService, caseService, precedentService } from './api';

describe('API Client', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
    mockPost.mockClear();
    mockGet.mockClear();
    mockPut.mockClear();
  });

  describe('authService', () => {
    it('should call login endpoint with correct data', async () => {
      const mockResponse = {
        data: {
          access_token: 'test-token',
          token_type: 'bearer',
          user_id: 'user-123',
          role: 'CITIZEN',
        },
      };

      mockPost.mockResolvedValueOnce(mockResponse);
      
      const result = await authService.login('test@example.com', 'password123');

      expect(mockPost).toHaveBeenCalledWith('/auth/login', {
        email: 'test@example.com',
        password: 'password123',
      });
      expect(result).toEqual(mockResponse.data);
    });

    it('should call register endpoint with correct data', async () => {
      const mockResponse = {
        data: {
          access_token: 'test-token',
          token_type: 'bearer',
          user_id: 'user-123',
          role: 'CITIZEN',
        },
      };

      mockPost.mockResolvedValueOnce(mockResponse);
      
      const result = await authService.register('test@example.com', 'password123', 'CITIZEN');

      expect(mockPost).toHaveBeenCalledWith('/auth/register', {
        email: 'test@example.com',
        password: 'password123',
        role: 'CITIZEN',
      });
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('caseService', () => {
    it('should create case with correct data', async () => {
      const mockCase = {
        id: 'case-123',
        title: 'Test Case',
        description: 'Test Description',
        status: 'FILED',
        user_id: 'user-123',
        priority: 'REGULAR',
        created_at: '2024-01-01T00:00:00Z',
      };

      mockPost.mockResolvedValueOnce({ data: mockCase });
      
      const result = await caseService.createCase('Test Case', 'Test Description');

      expect(mockPost).toHaveBeenCalledWith('/cases', {
        title: 'Test Case',
        description: 'Test Description',
      });
      expect(result).toEqual(mockCase);
    });

    it('should fetch cases list', async () => {
      const mockCases = [
        {
          id: 'case-1',
          title: 'Case 1',
          description: 'Description 1',
          status: 'FILED',
          user_id: 'user-123',
          created_at: '2024-01-01T00:00:00Z',
        },
      ];

      mockGet.mockResolvedValueOnce({ data: mockCases });
      
      const result = await caseService.getCases();

      expect(mockGet).toHaveBeenCalledWith('/cases', {
        params: { page: 1, limit: 50 },
      });
      expect(result).toEqual(mockCases);
    });

    it('should fetch case by id', async () => {
      const mockCase = {
        id: 'case-123',
        title: 'Test Case',
        description: 'Test Description',
        status: 'FILED',
        user_id: 'user-123',
        priority: 'REGULAR',
        created_at: '2024-01-01T00:00:00Z',
      };

      mockGet.mockResolvedValueOnce({ data: mockCase });
      
      const result = await caseService.getCaseById('case-123');

      expect(mockGet).toHaveBeenCalledWith('/cases/case-123');
      expect(result).toEqual(mockCase);
    });
  });

  describe('precedentService', () => {
    it('should search precedents', async () => {
      const mockResults = [
        {
          case_name: 'Case A',
          summary: 'Summary A',
          relevance_score: 0.95,
        },
      ];

      mockGet.mockResolvedValueOnce({ data: mockResults });
      
      const result = await precedentService.search('property dispute');

      expect(mockGet).toHaveBeenCalledWith('/precedents/search', {
        params: { q: 'property dispute', limit: 5 },
      });
      expect(result).toEqual(mockResults);
    });
  });
});
