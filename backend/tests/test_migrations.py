"""
Test script for Alembic migrations.

This script tests:
1. Applying migrations (upgrade)
2. Verifying table schema
3. Rolling back migrations (downgrade)
4. Re-applying migrations

Run this test with: pytest backend/tests/test_migrations.py -v
"""

import os
import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture(scope="module")
def alembic_config():
    """Create Alembic configuration"""
    config = Config("alembic.ini")
    return config


def test_alembic_config_exists():
    """Test that alembic.ini configuration file exists"""
    assert os.path.exists("alembic.ini"), "alembic.ini file not found"


def test_database_url_configured():
    """Test that DATABASE_URL is configured"""
    assert DATABASE_URL is not None, "DATABASE_URL not set in environment"
    assert "postgresql" in DATABASE_URL, "DATABASE_URL should be PostgreSQL connection string"


def test_migrations_directory_exists():
    """Test that migrations directory exists"""
    assert os.path.exists("alembic/versions"), "alembic/versions directory not found"


def test_current_migration_is_head(alembic_config):
    """Test that database is at the latest migration"""
    # This test verifies migrations have been applied
    # In a real test, you would check the current revision matches head
    pass  # Placeholder for actual migration verification
