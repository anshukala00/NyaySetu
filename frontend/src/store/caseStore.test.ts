import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useCaseStore } from './caseStore';
import apiClient from '../services/api';

// Mock the API client
vi.mock('../services/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Case Store', () => {
  beforeEach(() => {
    useCaseStore.setState({
      cases: [],
      currentCase: null,
      loading: false,
      error: null,
    });
    vi.clearAllMocks();
  });

  it('should initialize with default state', () => {
    const state = useCaseStore.getState();
    expect(state.cases).toEqual([]);
    expect(state.currentCase).toBeNull();
    expect(state.loading).toBe(false);
    expect(state.error).toBeNull();
  });

  it('should fetch cases successfully', async () => {
    const mockCases = [
      {
        id: 'case-1',
        title: 'Case 1',
        description: 'Description 1',
        status: 'FILED',
        user_id: 'user-123',
        judge_id: null,
        priority: null,
        ai_summary: null,
        created_at: '2024-01-01T00:00:00Z',
      },
      {
        id: 'case-2',
        title: 'Case 2',
        description: 'Description 2',
        status: 'IN_REVIEW',
        user_id: 'user-123',
        judge_id: 'judge-123',
        priority: 'HIGH',
        ai_summary: null,
        created_at: '2024-01-02T00:00:00Z',
      },
    ];

    vi.mocked(apiClient.get).mockResolvedValueOnce({ data: mockCases });

    const store = useCaseStore.getState();
    await store.fetchCases();

    const state = useCaseStore.getState();
    expect(state.cases).toEqual(mockCases);
    expect(state.loading).toBe(false);
  });

  it('should fetch case by id successfully', async () => {
    const mockCase = {
      id: 'case-123',
      title: 'Test Case',
      description: 'Test Description',
      status: 'FILED',
      user_id: 'user-123',
      judge_id: null,
      priority: 'HIGH',
      ai_summary: null,
      created_at: '2024-01-01T00:00:00Z',
    };

    vi.mocked(apiClient.get).mockResolvedValueOnce({ data: mockCase });

    const store = useCaseStore.getState();
    await store.fetchCaseById('case-123');

    const state = useCaseStore.getState();
    expect(state.currentCase).toEqual(mockCase);
    expect(state.loading).toBe(false);
  });

  it('should create case successfully', async () => {
    const newCase = {
      id: 'case-new',
      title: 'New Case',
      description: 'New Description',
      status: 'FILED',
      user_id: 'user-123',
      judge_id: null,
      priority: 'REGULAR',
      ai_summary: null,
      created_at: '2024-01-03T00:00:00Z',
    };

    vi.mocked(apiClient.post).mockResolvedValueOnce({ data: newCase });

    const store = useCaseStore.getState();
    await store.createCase('New Case', 'New Description');

    const state = useCaseStore.getState();
    expect(state.cases[0]).toEqual(newCase);
    expect(state.loading).toBe(false);
  });

  it('should add case to store', () => {
    const testCase = {
      id: 'case-123',
      title: 'Test Case',
      description: 'Test Description',
      status: 'FILED',
      user_id: 'user-123',
      judge_id: null,
      priority: null,
      ai_summary: null,
      created_at: '2024-01-01T00:00:00Z',
    };

    const store = useCaseStore.getState();
    store.addCase(testCase);

    const state = useCaseStore.getState();
    expect(state.cases[0]).toEqual(testCase);
  });

  it('should update case in store', () => {
    const initialCase = {
      id: 'case-123',
      title: 'Test Case',
      description: 'Test Description',
      status: 'FILED',
      user_id: 'user-123',
      judge_id: null,
      priority: null,
      ai_summary: null,
      created_at: '2024-01-01T00:00:00Z',
    };

    useCaseStore.setState({ cases: [initialCase], currentCase: initialCase });

    const updatedCase = { ...initialCase, status: 'IN_REVIEW' };

    const store = useCaseStore.getState();
    store.updateCase(updatedCase);

    const state = useCaseStore.getState();
    expect(state.cases[0].status).toBe('IN_REVIEW');
    expect(state.currentCase?.status).toBe('IN_REVIEW');
  });

  it('should generate summary successfully', async () => {
    const initialCase = {
      id: 'case-123',
      title: 'Test Case',
      description: 'Test Description',
      status: 'FILED',
      user_id: 'user-123',
      judge_id: null,
      priority: null,
      ai_summary: null,
      created_at: '2024-01-01T00:00:00Z',
    };

    useCaseStore.setState({ currentCase: initialCase });

    const mockResponse = {
      data: {
        summary: 'Test summary [AI Generated Summary]',
      },
    };

    vi.mocked(apiClient.post).mockResolvedValueOnce(mockResponse);

    const store = useCaseStore.getState();
    await store.generateSummary('case-123');

    const state = useCaseStore.getState();
    expect(state.currentCase?.ai_summary).toBe('Test summary [AI Generated Summary]');
    expect(state.loading).toBe(false);
  });

  it('should clear error', () => {
    useCaseStore.setState({ error: 'Test error' });

    const store = useCaseStore.getState();
    store.clearError();

    const state = useCaseStore.getState();
    expect(state.error).toBeNull();
  });

  it('should handle fetch cases error', async () => {
    const mockError = new Error('Failed to fetch cases');

    vi.mocked(apiClient.get).mockRejectedValueOnce(mockError);

    const store = useCaseStore.getState();
    try {
      await store.fetchCases();
    } catch (error) {
      // Expected error
    }

    const state = useCaseStore.getState();
    expect(state.error).toBe('Failed to fetch cases');
    expect(state.loading).toBe(false);
  });

  it('should handle create case error', async () => {
    const mockError = new Error('Failed to create case');

    vi.mocked(apiClient.post).mockRejectedValueOnce(mockError);

    const store = useCaseStore.getState();
    try {
      await store.createCase('Test', 'Test');
    } catch (error) {
      // Expected error
    }

    const state = useCaseStore.getState();
    expect(state.error).toBe('Failed to create case');
    expect(state.loading).toBe(false);
  });
});
