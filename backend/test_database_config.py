"""
Test script to verify database configuration and connection pooling.

This script tests:
1. Database connection is successful
2. Connection pooling is configured correctly
3. SessionLocal can create sessions
4. get_db() dependency function works
"""

import sys
from sqlalchemy import text
from app.database import engine, SessionLocal, get_db, Base

def test_database_connection():
    """Test basic database connection."""
    print("Testing database connection...")
    try:
        # Test connection by executing a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_connection_pool():
    """Test connection pool configuration."""
    print("\nTesting connection pool configuration...")
    try:
        pool = engine.pool
        print(f"✓ Pool size: {pool.size()}")
        print(f"✓ Max overflow: {pool._max_overflow}")
        print(f"✓ Pool timeout: {pool._timeout}")
        print(f"✓ Pool pre-ping enabled: {engine.pool_pre_ping}")
        return True
    except Exception as e:
        print(f"✗ Connection pool test failed: {e}")
        return False

def test_session_creation():
    """Test SessionLocal can create sessions."""
    print("\nTesting session creation...")
    try:
        db = SessionLocal()
        print("✓ SessionLocal created successfully")
        
        # Test a simple query
        result = db.execute(text("SELECT 1"))
        print("✓ Session can execute queries")
        
        db.close()
        print("✓ Session closed successfully")
        return True
    except Exception as e:
        print(f"✗ Session creation failed: {e}")
        return False

def test_get_db_dependency():
    """Test get_db() dependency function."""
    print("\nTesting get_db() dependency function...")
    try:
        # Simulate FastAPI dependency usage
        db_generator = get_db()
        db = next(db_generator)
        print("✓ get_db() yielded session successfully")
        
        # Test query
        result = db.execute(text("SELECT 1"))
        print("✓ Session from get_db() can execute queries")
        
        # Close the generator (simulates end of request)
        try:
            next(db_generator)
        except StopIteration:
            print("✓ get_db() properly closes session")
        
        return True
    except Exception as e:
        print(f"✗ get_db() test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Database Configuration Test Suite")
    print("=" * 60)
    
    tests = [
        test_database_connection,
        test_connection_pool,
        test_session_creation,
        test_get_db_dependency
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Database configuration is correct.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
