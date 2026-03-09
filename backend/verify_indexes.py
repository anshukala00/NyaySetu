"""Verify database indexes are properly created"""
from sqlalchemy import text
from app.database import SessionLocal

db = SessionLocal()

try:
    # Check indexes
    result = db.execute(text("""
        SELECT tablename, indexname, indexdef 
        FROM pg_indexes 
        WHERE schemaname = 'public' 
        ORDER BY tablename, indexname;
    """))
    
    print("=" * 80)
    print("DATABASE INDEXES")
    print("=" * 80)
    
    for row in result:
        print(f"\nTable: {row[0]}")
        print(f"Index: {row[1]}")
        print(f"Definition: {row[2]}")
    
    print("\n" + "=" * 80)
    print("✓ Index verification complete")
    print("=" * 80)
    
finally:
    db.close()
