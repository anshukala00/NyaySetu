"""
Test script to verify PostgreSQL database connection
Run this after setting up the database to ensure everything is configured correctly
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection using credentials from .env file"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in .env file")
        print("Please ensure your .env file contains:")
        print("DATABASE_URL=postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu")
        return False
    
    print("🔍 Testing database connection...")
    print(f"Connection string: {database_url.replace(database_url.split('@')[0].split('//')[1], '***:***')}")
    
    try:
        # Parse the connection string
        # Format: postgresql://user:password@host:port/database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("\n✅ Connection successful!")
        print(f"PostgreSQL version: {db_version[0]}")
        
        # Check if we can create tables (permissions test)
        cursor.execute("""
            SELECT has_schema_privilege('public', 'CREATE');
        """)
        can_create = cursor.fetchone()[0]
        
        if can_create:
            print("✅ User has CREATE privileges on public schema")
        else:
            print("⚠️  WARNING: User does not have CREATE privileges")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n🎉 Database setup is complete and working!")
        print("\nNext steps:")
        print("1. Run database migrations: alembic upgrade head")
        print("2. Start the backend server: uvicorn app.main:app --reload")
        
        return True
        
    except OperationalError as e:
        print("\n❌ Connection failed!")
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify PostgreSQL is running")
        print("2. Check database name, username, and password in .env")
        print("3. Ensure the database 'nyaysetu' exists")
        print("4. Verify user 'nyaysetu_user' has been created")
        print("5. Check if port 5432 is correct")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
