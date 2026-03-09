#!/usr/bin/env python3
"""
Test script to verify FastAPI project initialization
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import fastapi
        print(f"✓ FastAPI {fastapi.__version__} imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✓ Uvicorn imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Uvicorn: {e}")
        return False
    
    try:
        import sqlalchemy
        print(f"✓ SQLAlchemy {sqlalchemy.__version__} imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import SQLAlchemy: {e}")
        return False
    
    try:
        import pydantic
        print(f"✓ Pydantic imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Pydantic: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print(f"✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import python-dotenv: {e}")
        return False
    
    return True

def test_app_structure():
    """Test that the FastAPI app can be loaded"""
    print("\nTesting FastAPI application structure...")
    
    try:
        from app.main import app
        print(f"✓ FastAPI app loaded successfully")
        print(f"  - Title: {app.title}")
        print(f"  - Version: {app.version}")
        return True
    except Exception as e:
        print(f"✗ Failed to load FastAPI app: {e}")
        return False

def test_env_config():
    """Test that environment configuration is loaded"""
    print("\nTesting environment configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import os
        jwt_secret = os.getenv("JWT_SECRET")
        cors_origins = os.getenv("CORS_ORIGINS")
        
        if jwt_secret:
            print(f"✓ JWT_SECRET is configured")
        else:
            print(f"⚠ JWT_SECRET is not set")
        
        if cors_origins:
            print(f"✓ CORS_ORIGINS is configured: {cors_origins}")
        else:
            print(f"⚠ CORS_ORIGINS is not set")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load environment config: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("FastAPI Project Initialization Test")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test app structure
    results.append(test_app_structure())
    
    # Test environment config
    results.append(test_env_config())
    
    # Summary
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All tests passed! FastAPI project is properly initialized.")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
