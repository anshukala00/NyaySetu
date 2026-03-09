# Nyaysetu Case Management System - Backend

FastAPI backend for the Nyaysetu judicial case management system.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 15 or higher
- pip (Python package manager)

## Setup

### 1. Database Setup

**Quick Setup (Windows)**:
```cmd
cd scripts
setup_database.bat
```

**Manual Setup**:
```cmd
psql -U postgres -f scripts/init_db.sql
```

For detailed instructions, see:
- Quick guide: `../docs/QUICK_START_DATABASE.md`
- Full guide: `../docs/database-setup-windows.md`

### 2. Python Environment

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate.ps1`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration

1. Create a `.env` file based on `.env.example`:
```bash
copy .env.example .env
```

2. Update the `.env` file with your database credentials:
```env
DATABASE_URL=postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000
```

### 4. Database Migrations

Alembic is configured to automatically read `DATABASE_URL` from the `.env` file and detect model changes.

**Important**: Before creating migrations, ensure all models are imported in `alembic/env.py`.

Run Alembic migrations to create tables:
```bash
alembic upgrade head
```

For detailed migration workflow and commands, see `alembic/README.md`.

### 5. Verify Setup

Test database connection:
```bash
python test_db_connection.py
```

You should see: ✅ Connection successful!

### 6. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application entry point
├── models/              # SQLAlchemy database models
├── services/            # Business logic services
├── routes/              # API route handlers
├── scripts/             # Database setup scripts
│   ├── init_db.sql      # PostgreSQL initialization
│   ├── setup_database.bat  # Windows setup script
│   └── README.md        # Scripts documentation
├── tests/               # Test files
├── requirements.txt     # Python dependencies
├── test_db_connection.py  # Database connection test
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Database

### Connection Details

- **Database**: nyaysetu
- **User**: nyaysetu_user
- **Password**: nyaysetu_pass (development only)
- **Host**: localhost
- **Port**: 5432

### Database Schema

The system uses two main tables:
- `users`: User accounts (citizens and judges)
- `cases`: Legal cases filed by citizens

Migrations are managed with Alembic.

### Common Database Commands

```bash
# Check current migration version
alembic current

# Check if database is in sync with models
alembic check

# Create a new migration (autogenerate from model changes)
alembic revision --autogenerate -m "description"

# Create a new migration (manual)
alembic revision -m "description"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# View migration history
alembic history

# View SQL without executing
alembic upgrade head --sql
```

For more details on migrations, see `alembic/README.md`.

## Testing

Run tests with:
```bash
pytest
```
