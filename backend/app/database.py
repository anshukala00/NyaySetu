"""
Database configuration module for Nyaysetu Case Management System.

This module sets up SQLAlchemy engine with connection pooling as per NFR6.1:
- pool_size=5
- max_overflow=10
- Connection timeout: 30 seconds

Validates: Requirements NFR6.1
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read DATABASE_URL from environment variables (DR1, DR2)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please configure it in the .env file."
    )

# Create SQLAlchemy engine with connection pooling (NFR6.1)
# pool_size=5: Number of connections to keep open in the pool
# max_overflow=10: Maximum number of connections that can be created beyond pool_size
# pool_timeout=30: Connection timeout in seconds
# pool_pre_ping=True: Verify connections before using them (handles stale connections)
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
    echo=False  # Set to True for SQL query logging during development
)

# Create SessionLocal class for database sessions
# autocommit=False: Transactions must be explicitly committed
# autoflush=False: Changes are not automatically flushed to the database
# bind=engine: Bind sessions to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
# All SQLAlchemy models will inherit from this Base class
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    
    This function is used as a FastAPI dependency to provide
    database sessions to route handlers. It ensures that the
    session is properly closed after the request is completed.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/api/cases")
        def get_cases(db: Session = Depends(get_db)):
            cases = db.query(Case).all()
            return cases
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
