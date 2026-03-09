"""
Test Alembic configuration.

This test verifies that Alembic is properly configured to:
- Read DATABASE_URL from environment variables
- Import Base metadata for autogenerate support
- Connect to the database successfully

Validates: Requirements NFR4.3
"""

import os
import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


def test_alembic_config_exists():
    """Test that alembic.ini configuration file exists."""
    import os.path
    alembic_ini_path = os.path.join(os.path.dirname(__file__), '..', 'alembic.ini')
    assert os.path.exists(alembic_ini_path), "alembic.ini file should exist"


def test_alembic_env_imports_base():
    """Test that alembic/env.py imports Base metadata."""
    env_path = os.path.join(os.path.dirname(__file__), '..', 'alembic', 'env.py')
    
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    # Check that Base is imported
    assert 'from app.database import Base' in env_content, \
        "env.py should import Base from app.database"
    
    # Check that target_metadata is set to Base.metadata
    assert 'target_metadata = Base.metadata' in env_content, \
        "env.py should set target_metadata to Base.metadata"
    
    # Check that DATABASE_URL is loaded from environment
    assert 'os.getenv("DATABASE_URL")' in env_content, \
        "env.py should load DATABASE_URL from environment"


def test_alembic_can_connect_to_database():
    """Test that Alembic can connect to the database using DATABASE_URL."""
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    assert database_url is not None, "DATABASE_URL should be set in .env file"
    
    # Test database connection
    engine = create_engine(database_url)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1, "Database connection should work"
    finally:
        engine.dispose()


def test_alembic_script_directory_exists():
    """Test that Alembic versions directory exists."""
    versions_path = os.path.join(os.path.dirname(__file__), '..', 'alembic', 'versions')
    assert os.path.exists(versions_path), "alembic/versions directory should exist"


def test_alembic_config_loads():
    """Test that Alembic configuration loads without errors."""
    alembic_ini_path = os.path.join(os.path.dirname(__file__), '..', 'alembic.ini')
    
    # Load Alembic config
    config = Config(alembic_ini_path)
    
    # Verify script location is set
    script_location = config.get_main_option("script_location")
    assert script_location is not None, "script_location should be configured"
    
    # Verify ScriptDirectory can be created
    script = ScriptDirectory.from_config(config)
    assert script is not None, "ScriptDirectory should be created successfully"


def test_database_url_format():
    """Test that DATABASE_URL has correct PostgreSQL format."""
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    assert database_url is not None, "DATABASE_URL should be set"
    assert database_url.startswith("postgresql://"), \
        "DATABASE_URL should start with postgresql://"
    
    # Check that it contains required components
    assert "@" in database_url, "DATABASE_URL should contain @ for user/host separator"
    assert "/" in database_url.split("@")[1], \
        "DATABASE_URL should contain database name after host"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
