import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CaseForm } from './CaseForm';

// Mock the API
vi.mock('../../services/api', () => ({
  caseService: {
    createCase: vi.fn(),
  },
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

// Mock the case store
let mockAddCase = vi.fn();

vi.mock('../../store/caseStore', () => ({
  useCaseStore: vi.fn((selector: any) => {
    const mockStore = {
      addCase: mockAddCase,
    };
    if (typeof selector === 'function') {
      return selector(mockStore);
    }
    return mockStore;
  }),
}));

describe('CaseForm', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockAddCase.mockClear();
  });

  it('should render case form with title and description fields', () => {
    render(<CaseForm />);

    expect(screen.getByText('File a New Case')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter case title')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Describe your case in detail...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /file case/i })).toBeInTheDocument();
  });

  it('should display character counter for title field', async () => {
    const user = userEvent.setup();
    render(<CaseForm />);

    const titleInput = screen.getByPlaceholderText('Enter case title');
    await user.type(titleInput, 'Test Case Title');

    expect(screen.getByText(/15\/200/)).toBeInTheDocument();
  });

  it('should display character counter for description field', async () => {
    const user = userEvent.setup();
    render(<CaseForm />);

    const descriptionInput = screen.getByPlaceholderText('Describe your case in detail...');
    await user.type(descriptionInput, 'Test description');

    expect(screen.getByText('16/10,000')).toBeInTheDocument();
  });

  it('should enforce title max length of 200 characters', async () => {
    const user = userEvent.setup();
    render(<CaseForm />);

    const titleInput = screen.getByPlaceholderText('Enter case title') as HTMLInputElement;
    const longTitle = 'a'.repeat(250);

    await user.type(titleInput, longTitle);

    expect(titleInput.value.length).toBeLessThanOrEqual(200);
  });

  it('should enforce description max length of 10,000 characters', async () => {
    const user = userEvent.setup();
    render(<CaseForm />);

    const descriptionInput = screen.getByPlaceholderText('Describe your case in detail...') as HTMLTextAreaElement;
    const longDescription = 'a'.repeat(15000);

    // Use paste instead of type for performance
    await user.click(descriptionInput);
    await user.paste(longDescription);

    expect(descriptionInput.value.length).toBeLessThanOrEqual(10000);
  });

  it('should display validation error when title is empty', async () => {
    const user = userEvent.setup();
    render(<CaseForm />);

    const submitButton = screen.getByRole('button', { name: /file case/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Case title is required')).toBeInTheDocument();
    }, { timeout: 2000 });
  });

  it('should display validation error when description is empty', async () => {
    const user = userEvent.setup();
    render(<CaseForm />);

    const titleInput = screen.getByPlaceholderText('Enter case title');
    await user.type(titleInput, 'Test Case');

    const submitButton = screen.getByRole('button', { name: /file case/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Case description is required')).toBeInTheDocument();
    }, { timeout: 2000 });
  });

  it('should successfully submit form with valid data', async () => {
    const user = userEvent.setup();
    const { caseService } = await import('../../services/api');
    const mockResponse = {
      id: 'case-123',
      title: 'Test Case',
      description: 'Test Description',
      status: 'FILED',
      user_id: 'user-123',
      priority: 'REGULAR',
      created_at: '2024-01-01T00:00:00Z',
    };

    vi.mocked(caseService.createCase).mockResolvedValueOnce(mockResponse);

    render(<CaseForm />);

    const titleInput = screen.getByPlaceholderText('Enter case title');
    const descriptionInput = screen.getByPlaceholderText('Describe your case in detail...');
    const submitButton = screen.getByRole('button', { name: /file case/i });

    await user.type(titleInput, 'Test Case');
    await user.type(descriptionInput, 'Test Description');
    await user.click(submitButton);

    await waitFor(() => {
      expect(caseService.createCase).toHaveBeenCalledWith('Test Case', 'Test Description');
    });

    await waitFor(() => {
      expect(screen.getByText('Case filed successfully!')).toBeInTheDocument();
      expect(screen.getByText('Case ID: case-123')).toBeInTheDocument();
    });
  });

  it('should display error message on submission failure', async () => {
    const user = userEvent.setup();
    const { caseService } = await import('../../services/api');
    const mockError = {
      response: {
        data: { detail: 'Failed to file case' },
      },
    };

    vi.mocked(caseService.createCase).mockRejectedValueOnce(mockError);

    render(<CaseForm />);

    const titleInput = screen.getByPlaceholderText('Enter case title');
    const descriptionInput = screen.getByPlaceholderText('Describe your case in detail...');
    const submitButton = screen.getByRole('button', { name: /file case/i });

    await user.type(titleInput, 'Test Case');
    await user.type(descriptionInput, 'Test Description');
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Failed to file case')).toBeInTheDocument();
    });
  });

  it('should show loading state while submitting', async () => {
    const user = userEvent.setup();
    const { caseService } = await import('../../services/api');
    const mockResponse = {
      id: 'case-123',
      title: 'Test Case',
      description: 'Test Description',
      status: 'FILED',
      user_id: 'user-123',
      priority: 'REGULAR',
      created_at: '2024-01-01T00:00:00Z',
    };

    vi.mocked(caseService.createCase).mockImplementationOnce(
      () => new Promise(resolve => setTimeout(() => resolve(mockResponse), 100))
    );

    render(<CaseForm />);

    const titleInput = screen.getByPlaceholderText('Enter case title');
    const descriptionInput = screen.getByPlaceholderText('Describe your case in detail...');
    const submitButton = screen.getByRole('button', { name: /file case/i });

    await user.type(titleInput, 'Test Case');
    await user.type(descriptionInput, 'Test Description');
    await user.click(submitButton);

    expect(screen.getByText('Filing Case...')).toBeInTheDocument();
    expect(submitButton).toBeDisabled();
  });

  it('should clear form when clear button is clicked', async () => {
    const user = userEvent.setup();
    render(<CaseForm />);

    const titleInput = screen.getByPlaceholderText('Enter case title') as HTMLInputElement;
    const descriptionInput = screen.getByPlaceholderText('Describe your case in detail...') as HTMLTextAreaElement;
    const clearButton = screen.getByRole('button', { name: /clear/i });

    await user.type(titleInput, 'Test Case');
    await user.type(descriptionInput, 'Test Description');

    expect(titleInput.value).toBe('Test Case');
    expect(descriptionInput.value).toBe('Test Description');

    await user.click(clearButton);

    await waitFor(() => {
      expect(titleInput.value).toBe('');
      expect(descriptionInput.value).toBe('');
    });
  });

  it('should display category dropdown', () => {
    render(<CaseForm />);

    const categorySelect = screen.getByDisplayValue('Select a category');
    expect(categorySelect).toBeInTheDocument();
  });

  it('should allow category selection', async () => {
    const user = userEvent.setup();
    render(<CaseForm />);

    const categorySelect = screen.getByDisplayValue('Select a category');
    await user.selectOptions(categorySelect, 'civil');

    expect((categorySelect as HTMLSelectElement).value).toBe('civil');
  });

  it('should display voice input button', () => {
    render(<CaseForm />);

    const voiceButton = screen.getByRole('button', { name: /add via voice/i });
    expect(voiceButton).toBeInTheDocument();
  });

  it('should display info box with next steps', () => {
    render(<CaseForm />);

    expect(screen.getByText('What happens next?')).toBeInTheDocument();
    expect(screen.getByText(/your case will be analyzed by our ai triage system/i)).toBeInTheDocument();
  });
});
