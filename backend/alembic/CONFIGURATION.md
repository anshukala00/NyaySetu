# Alembic Configuration Summary

This document describes the Alembic configuration for the Nyaysetu Case Management System.

## Configuration Overview

Alembic has been configured to meet the requirements specified in **NFR4.3**: "Database schema changes shall be managed via Alembic migrations"

## Key Configuration Changes

### 1. alembic.ini
- **Location**: `backend/alembic.ini`
- **Changes**: Updated placeholder database URL with PostgreSQL format
- **Note**: The actual DATABASE_URL is loaded from `.env` file in `env.py`, not from this file

### 2. alembic/env.py
The following enhancements were made to `env.py`:

#### a. Environment Variable Loading
```python
from dotenv import load_dotenv
load_dotenv()
```
- Loads DATABASE_URL from `.env` file automatically
- No need to manually configure database URL in alembic.ini

#### b. Path Configuration
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
```
- Adds parent directory to Python path
- Allows importing app modules and models

#### c. Base Metadata Import
```python
from app.database import Base
target_metadata = Base.metadata
```
- Imports SQLAlchemy Base from database module
- Enables autogenerate feature to detect model changes

#### d. Database URL Override
```python
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
```
- Overrides alembic.ini database URL with environment variable
- Uses same DATABASE_URL as the application

### 3. Model Import Section
```python
# Import all models here so Alembic can detect them for autogenerate
# When models are created, import them here:
# from models.user import User
# from models.case import Case
```
- Placeholder for model imports
- Models must be imported here for autogenerate to work
- Will be updated when User and Case models are created

## Features Enabled

### ✅ Autogenerate Support
Alembic can now automatically detect model changes and generate migration scripts:
```bash
alembic revision --autogenerate -m "Create users table"
```

### ✅ Environment Variable Integration
Database URL is read from `.env` file, same as the application:
```env
DATABASE_URL=postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu
```

### ✅ Model Change Detection
When models are imported in `env.py`, Alembic can detect:
- New tables
- New columns
- Column type changes
- Index changes
- Foreign key changes
- Constraint changes

### ✅ Database Connection Pooling
Uses the same SQLAlchemy engine configuration as the application:
- pool_size=5
- max_overflow=10
- pool_timeout=30 seconds
- pool_pre_ping=True

## Verification

The configuration has been verified with:

1. **Connection Test**: `alembic current` - Successfully connects to database
2. **Check Command**: `alembic check` - No errors, ready for migrations
3. **Unit Tests**: `tests/test_alembic_config.py` - All 6 tests pass

## Next Steps

To use Alembic for migrations:

1. **Create Models** (Task 2.1, 2.2)
   - Define User and Case models in `models/` directory
   - Inherit from `app.database.Base`

2. **Import Models in env.py** (Part of Task 2.3)
   - Add imports to `alembic/env.py`:
   ```python
   from models.user import User
   from models.case import Case
   ```

3. **Generate Initial Migration** (Task 1.2.4, 2.3.1, 2.3.2)
   ```bash
   alembic revision --autogenerate -m "Create users and cases tables"
   ```

4. **Review Migration**
   - Check generated file in `alembic/versions/`
   - Verify upgrade() and downgrade() functions

5. **Apply Migration**
   ```bash
   alembic upgrade head
   ```

## Requirements Validation

This configuration satisfies:

- **NFR4.3**: Database schema changes shall be managed via Alembic migrations ✅
- **Design Section**: "Database schema changes should be managed via Alembic migrations" ✅
- **Design Section**: "Alembic should use the same DATABASE_URL as SQLAlchemy" ✅
- **Design Section**: "Configure to auto-detect model changes" ✅

## References

- Design Document: `.kiro/specs/nyaysetu-case-management/design.md`
- Requirements: `.kiro/specs/nyaysetu-case-management/requirements.md`
- Alembic Documentation: https://alembic.sqlalchemy.org/
- Task: 1.2.3 Set up Alembic for database migrations
