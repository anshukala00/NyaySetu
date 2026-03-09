import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CaseList } from './CaseList';

// Mock the case store
const mockCases = [
  {
    id: 'case-1',
    title: 'Property Dispute',
    description: 'Dispute over property boundary',
    status: 'FILED',
    user_id: 'user-123',
    judge_id: null,
    priority: 'HIGH',
    ai_summary: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'case-2',
    title: 'Contract Breach',
    description: 'Breach of service contract',
    status: 'IN_REVIEW',
    user_id: 'user-123',
    judge_id: 'judge-123',
    priority: 'REGULAR',
    ai_summary: 'Summary text',
    created_at: '2024-01-02T00:00:00Z',
  },
  {
    id: 'case-3',
    title: 'Family Matter',
    description: 'Custody dispute',
    status: 'HEARING_SCHEDULED',
    user_id: 'user-123',
    judge_id: 'judge-123',
    priority: null,
    ai_summary: null,
    created_at: '2024-01-03T00:00:00Z',
  },
];

let mockStoreState = {
  cases: mockCases,
  loading: false,
};

vi.mock('../../store/caseStore', () => ({
  useCaseStore: vi.fn((selector: any) => {
    if (typeof selector === 'function') {
      return selector(mockStoreState);
    }
    return mockStoreState;
  }),
}));

describe('CaseList', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset mock store state
    mockStoreState = {
      cases: mockCases,
      loading: false,
    };
  });

  it('should render case list with all cases', () => {
    render(<CaseList />);

    expect(screen.getByText('My Cases')).toBeInTheDocument();
    expect(screen.getByText('Property Dispute')).toBeInTheDocument();
    expect(screen.getByText('Contract Breach')).toBeInTheDocument();
    expect(screen.getByText('Family Matter')).toBeInTheDocument();
  });

  it('should display case cards with correct information', () => {
    render(<CaseList />);

    expect(screen.getByText('Property Dispute')).toBeInTheDocument();
    expect(screen.getByText('Dispute over property boundary')).toBeInTheDocument();
    expect(screen.getByText('FILED')).toBeInTheDocument();
    expect(screen.getByText('HIGH')).toBeInTheDocument();
  });

  it('should display empty state when no cases', () => {
    // Update mock store state
    mockStoreState = {
      cases: [],
      loading: false,
    };

    render(<CaseList />);

    expect(screen.getByText(/you haven't filed any cases yet/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /file your first case/i })).toBeInTheDocument();
  });

  it('should filter cases by search term', async () => {
    const user = userEvent.setup();
    render(<CaseList />);

    const searchInput = screen.getByPlaceholderText('Search cases by title...');
    await user.type(searchInput, 'Property');

    expect(screen.getByText('Property Dispute')).toBeInTheDocument();
    expect(screen.queryByText('Contract Breach')).not.toBeInTheDocument();
    expect(screen.queryByText('Family Matter')).not.toBeInTheDocument();
  });

  it('should filter cases by status', async () => {
    const user = userEvent.setup();
    render(<CaseList />);

    const filterSelect = screen.getByDisplayValue('All Cases');
    await user.selectOptions(filterSelect, 'FILED');

    expect(screen.getByText('Property Dispute')).toBeInTheDocument();
    expect(screen.queryByText('Contract Breach')).not.toBeInTheDocument();
    expect(screen.queryByText('Family Matter')).not.toBeInTheDocument();
  });

  it('should filter cases by IN_REVIEW status', async () => {
    const user = userEvent.setup();
    render(<CaseList />);

    const filterSelect = screen.getByDisplayValue('All Cases');
    await user.selectOptions(filterSelect, 'IN_REVIEW');

    expect(screen.queryByText('Property Dispute')).not.toBeInTheDocument();
    expect(screen.getByText('Contract Breach')).toBeInTheDocument();
    expect(screen.queryByText('Family Matter')).not.toBeInTheDocument();
  });

  it('should filter cases by HEARING_SCHEDULED status', async () => {
    const user = userEvent.setup();
    render(<CaseList />);

    const filterSelect = screen.getByDisplayValue('All Cases');
    await user.selectOptions(filterSelect, 'HEARING_SCHEDULED');

    expect(screen.queryByText('Property Dispute')).not.toBeInTheDocument();
    expect(screen.queryByText('Contract Breach')).not.toBeInTheDocument();
    expect(screen.getByText('Family Matter')).toBeInTheDocument();
  });

  it('should combine search and filter', async () => {
    const user = userEvent.setup();
    render(<CaseList />);

    const searchInput = screen.getByPlaceholderText('Search cases by title...');
    const filterSelect = screen.getByDisplayValue('All Cases');

    await user.type(searchInput, 'Dispute');
    await user.selectOptions(filterSelect, 'FILED');

    expect(screen.getByText('Property Dispute')).toBeInTheDocument();
    expect(screen.queryByText('Contract Breach')).not.toBeInTheDocument();
    expect(screen.queryByText('Family Matter')).not.toBeInTheDocument();
  });

  it('should display empty state when search has no results', async () => {
    const user = userEvent.setup();
    render(<CaseList />);

    const searchInput = screen.getByPlaceholderText('Search cases by title...');
    await user.type(searchInput, 'NonexistentCase');

    expect(screen.getByText(/no cases match your search or filter/i)).toBeInTheDocument();
  });

  it('should display status badges with correct colors', () => {
    render(<CaseList />);

    const filedBadge = screen.getByText('FILED');
    const inReviewBadge = screen.getByText('IN_REVIEW');
    const hearingBadge = screen.getByText('HEARING_SCHEDULED');

    expect(filedBadge).toHaveClass('bg-blue-100', 'text-blue-700');
    expect(inReviewBadge).toHaveClass('bg-yellow-100', 'text-yellow-700');
    expect(hearingBadge).toHaveClass('bg-green-100', 'text-green-700');
  });

  it('should display priority badges with correct colors', () => {
    render(<CaseList />);

    const highPriorityBadge = screen.getByText('HIGH');
    expect(highPriorityBadge).toHaveClass('bg-red-100', 'text-red-700');
  });

  it('should display AI summary indicator when available', () => {
    render(<CaseList />);

    const summaryIndicators = screen.getAllByText('AI Summary Available');
    expect(summaryIndicators.length).toBeGreaterThan(0);
  });

  it('should display filing date for each case', () => {
    render(<CaseList />);

    expect(screen.getByText(/filed on 1\/1\/2024/i)).toBeInTheDocument();
    expect(screen.getByText(/filed on 1\/2\/2024/i)).toBeInTheDocument();
    expect(screen.getByText(/filed on 1\/3\/2024/i)).toBeInTheDocument();
  });

  it('should display case ID for each case', () => {
    render(<CaseList />);

    expect(screen.getByText('Case ID: case-1')).toBeInTheDocument();
    expect(screen.getByText('Case ID: case-2')).toBeInTheDocument();
    expect(screen.getByText('Case ID: case-3')).toBeInTheDocument();
  });

  it('should be clickable to view case details', () => {
    render(<CaseList />);

    const caseCard = screen.getByText('Property Dispute').closest('.border.border-gray-200');
    expect(caseCard).toHaveClass('cursor-pointer');
  });

  it('should display search and filter inputs', () => {
    render(<CaseList />);

    expect(screen.getByPlaceholderText('Search cases by title...')).toBeInTheDocument();
    expect(screen.getByDisplayValue('All Cases')).toBeInTheDocument();
  });

  it('should truncate long descriptions', () => {
    render(<CaseList />);

    const descriptions = screen.getAllByText(/dispute/i);
    expect(descriptions.length).toBeGreaterThan(0);
  });
});
