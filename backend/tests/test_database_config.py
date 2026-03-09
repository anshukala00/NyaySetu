"""
Unit tests for database configuration module.

Tests verify that SQLAlchemy engine is properly configured with:
- Connection pooling (pool_size=5, max_overflow=10)
- Connection timeout (30 seconds)
- SessionLocal for database sessions
- Base for declarative models

Validates: Requirements NFR6.1
"""

import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base, get_db


class TestDatabaseConfiguration:
    """Test suite for database configuration."""

    def test_engine_exists(self):
        """Test that SQLAlchemy engine is created."""
        assert engine is not None
        assert str(engine.url).startswith("postgresql://")

    def test_connection_pool_size(self):
        """Test that connection pool size is set to 5 (NFR6.1)."""
        assert engine.pool.size() == 5

    def test_connection_pool_max_overflow(self):
        """Test that max overflow is set to 10 (NFR6.1)."""
        assert engine.pool._max_overflow == 10

    def test_connection_pool_timeout(self):
        """Test that connection timeout is set to 30 seconds (NFR6.1)."""
        assert engine.pool._timeout == 30

    def test_pool_pre_ping_enabled(self):
        """Test that pool_pre_ping is enabled for connection health checks."""
        assert engine.pool._pre_ping is True

    def test_session_local_exists(self):
        """Test that SessionLocal is created."""
        assert SessionLocal is not None

    def test_session_local_configuration(self):
        """Test that SessionLocal has correct configuration."""
        # Check that autocommit is False
        assert SessionLocal.kw.get("autocommit") is False
        # Check that autoflush is False
        assert SessionLocal.kw.get("autoflush") is False
        # Check that bind is set to engine
        assert SessionLocal.kw.get("bind") == engine

    def test_base_exists(self):
        """Test that Base for declarative models is created."""
        assert Base is not None

    def test_database_connection(self):
        """Test that database connection can be established."""
        conn = engine.connect()
        assert conn is not None
        conn.close()

    def test_get_db_dependency(self):
        """Test that get_db dependency function works correctly."""
        db_generator = get_db()
        db = next(db_generator)
        
        # Verify that db is a Session instance
        assert isinstance(db, Session)
        
        # Verify that session is bound to the engine
        assert db.bind == engine
        
        # Close the session
        try:
            next(db_generator)
        except StopIteration:
            pass  # Expected behavior

    def test_session_creation_and_closure(self):
        """Test that sessions can be created and closed properly."""
        db = SessionLocal()
        assert isinstance(db, Session)
        
        # Session should be usable
        assert db.bind == engine
        
        db.close()

    def test_multiple_sessions(self):
        """Test that multiple sessions can be created from SessionLocal."""
        db1 = SessionLocal()
        db2 = SessionLocal()
        
        assert db1 is not db2
        assert isinstance(db1, Session)
        assert isinstance(db2, Session)
        
        db1.close()
        db2.close()

    def test_connection_pool_reuse(self):
        """Test that connection pool reuses connections."""
        # Create and close multiple sessions to test pool reuse
        sessions = []
        for _ in range(3):
            db = SessionLocal()
            sessions.append(db)
        
        # Close all sessions
        for db in sessions:
            db.close()
        
        # Pool should have connections available for reuse
        assert engine.pool.size() == 5


class TestDatabaseURL:
    """Test suite for DATABASE_URL configuration."""

    def test_database_url_format(self):
        """Test that DATABASE_URL is in correct PostgreSQL format."""
        url = str(engine.url)
        assert url.startswith("postgresql://")
        assert "@localhost:5432/nyaysetu" in url

    def test_database_name(self):
        """Test that database name is 'nyaysetu'."""
        assert engine.url.database == "nyaysetu"

    def test_database_host(self):
        """Test that database host is 'localhost'."""
        assert engine.url.host == "localhost"

    def test_database_port(self):
        """Test that database port is 5432."""
        assert engine.url.port == 5432


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
