import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { RegisterPage } from './RegisterPage';

// Mock the API
vi.mock('../services/api', () => ({
  authService: {
    register: vi.fn(),
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

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('RegisterPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockNavigate.mockClear();
  });

  it('should render step 1 with email and password fields', () => {
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    expect(screen.getByText('Create Account')).toBeInTheDocument();
    expect(screen.getByText('Step 1 of 2')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('you@example.com')).toBeInTheDocument();
    expect(screen.getAllByPlaceholderText('••••••••')).toHaveLength(2);
  });

  it('should display validation errors for empty fields on step 1', async () => {
    const user = userEvent.setup();
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument();
      expect(screen.getByText('Password is required')).toBeInTheDocument();
    });
  });

  it('should display validation error for invalid email format', async () => {
    const user = userEvent.setup();
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByPlaceholderText('you@example.com');
    await user.type(emailInput, 'invalid-email');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Invalid email address')).toBeInTheDocument();
    });
  });

  it('should display validation error for short password', async () => {
    const user = userEvent.setup();
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const passwordInputs = screen.getAllByPlaceholderText('••••••••');
    await user.type(passwordInputs[0], 'short');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Password must be at least 8 characters')).toBeInTheDocument();
    });
  });

  it('should display validation error when passwords do not match', async () => {
    const user = userEvent.setup();
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const passwordInputs = screen.getAllByPlaceholderText('••••••••');
    await user.type(passwordInputs[0], 'password123');
    await user.type(passwordInputs[1], 'password456');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Passwords do not match')).toBeInTheDocument();
    });
  });

  it('should move to step 2 with valid credentials', async () => {
    const user = userEvent.setup();
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByPlaceholderText('you@example.com');
    const passwordInputs = screen.getAllByPlaceholderText('••••••••');

    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInputs[0], 'password123');
    await user.type(passwordInputs[1], 'password123');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Step 2 of 2')).toBeInTheDocument();
      expect(screen.getByText('Select Your Role')).toBeInTheDocument();
    });
  });

  it('should display role selection options on step 2', async () => {
    const user = userEvent.setup();
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByPlaceholderText('you@example.com');
    const passwordInputs = screen.getAllByPlaceholderText('••••••••');

    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInputs[0], 'password123');
    await user.type(passwordInputs[1], 'password123');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('👤 Citizen')).toBeInTheDocument();
      expect(screen.getByText('⚖️ Judge')).toBeInTheDocument();
    });
  });

  it('should allow role selection', async () => {
    const user = userEvent.setup();
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByPlaceholderText('you@example.com');
    const passwordInputs = screen.getAllByPlaceholderText('••••••••');

    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInputs[0], 'password123');
    await user.type(passwordInputs[1], 'password123');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      const judgeOption = screen.getByText('⚖️ Judge').closest('label');
      expect(judgeOption).toBeInTheDocument();
    });
  });

  it('should go back to step 1 from step 2', async () => {
    const user = userEvent.setup();
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByPlaceholderText('you@example.com');
    const passwordInputs = screen.getAllByPlaceholderText('••••••••');

    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInputs[0], 'password123');
    await user.type(passwordInputs[1], 'password123');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Step 2 of 2')).toBeInTheDocument();
    });

    const backButton = screen.getByRole('button', { name: /back/i });
    await user.click(backButton);

    await waitFor(() => {
      expect(screen.getByText('Step 1 of 2')).toBeInTheDocument();
    });
  });

  it('should successfully register with valid data', async () => {
    const user = userEvent.setup();
    const { authService } = await import('../services/api');
    vi.mocked(authService.register).mockResolvedValueOnce({
      access_token: 'test-token',
      token_type: 'bearer',
      user_id: 'user-123',
      role: 'CITIZEN',
    });

    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByPlaceholderText('you@example.com');
    const passwordInputs = screen.getAllByPlaceholderText('••••••••');

    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInputs[0], 'password123');
    await user.type(passwordInputs[1], 'password123');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Step 2 of 2')).toBeInTheDocument();
    });

    const createButton = screen.getByRole('button', { name: /create account/i });
    await user.click(createButton);

    await waitFor(() => {
      expect(authService.register).toHaveBeenCalledWith(
        'test@example.com',
        'password123',
        'CITIZEN'
      );
      expect(screen.getByText(/registration successful/i)).toBeInTheDocument();
    });
  });

  it('should display error message on registration failure', async () => {
    const user = userEvent.setup();
    const { authService } = await import('../services/api');
    const mockError = {
      response: {
        data: { detail: 'Email already registered' },
      },
    };

    vi.mocked(authService.register).mockRejectedValueOnce(mockError);

    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    const emailInput = screen.getByPlaceholderText('you@example.com');
    const passwordInputs = screen.getAllByPlaceholderText('••••••••');

    await user.type(emailInput, 'existing@example.com');
    await user.type(passwordInputs[0], 'password123');
    await user.type(passwordInputs[1], 'password123');

    const nextButton = screen.getByRole('button', { name: /next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Step 2 of 2')).toBeInTheDocument();
    });

    const createButton = screen.getByRole('button', { name: /create account/i });
    await user.click(createButton);

    await waitFor(() => {
      expect(screen.getByText('Email already registered')).toBeInTheDocument();
    });
  });

  it('should have login link', () => {
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    );

    expect(screen.getByText(/already have an account/i)).toBeInTheDocument();
    expect(screen.getByText(/sign in here/i)).toBeInTheDocument();
  });
});
