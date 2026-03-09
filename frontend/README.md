# Nyaysetu Frontend

React 18 + TypeScript + Vite frontend for the Nyaysetu Case Management System MVP.

## Tech Stack

- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Zustand**: State management
- **Tailwind CSS**: Styling
- **React Hook Form**: Form handling
- **Vitest**: Unit testing
- **React Testing Library**: Component testing

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable React components
│   ├── pages/          # Page-level components for routing
│   ├── services/       # API service functions
│   ├── store/          # Zustand store definitions
│   ├── types/          # TypeScript type definitions
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   └── index.css       # Global styles with Tailwind
├── index.html          # HTML entry point
├── package.json        # Dependencies and scripts
├── tsconfig.json       # TypeScript configuration
├── vite.config.ts      # Vite configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── postcss.config.js   # PostCSS configuration
└── .env                # Environment variables
```

## Environment Variables

Create a `.env` file in the frontend directory:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will open at `http://localhost:3000`

### Build

```bash
npm run build
```

### Testing

```bash
npm run test          # Run tests in watch mode
npm run test:run      # Run tests once
```

### Linting

```bash
npm run lint
```

## Features

- User authentication (login/register)
- Citizen portal for filing cases
- Judge dashboard for case management
- AI-powered case triage and summarization
- Precedent search functionality
- Role-based access control
- Responsive design with Tailwind CSS

## API Integration

The frontend communicates with the backend API at `http://localhost:8000/api`. The Axios client automatically:

- Attaches JWT tokens to requests
- Handles 401 errors by redirecting to login
- Provides a consistent error handling interface

## State Management

Zustand stores are used for:

- **authStore**: Authentication state and actions
- **caseStore**: Case management state and actions

## Testing

Tests are organized alongside source files with `.test.ts` or `.test.tsx` extensions.

## License

MIT
