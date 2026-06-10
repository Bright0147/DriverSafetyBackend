# clean_database.py
import sqlite3
import os

def clean_database():
    # Database path
    db_path = "data/driversafety.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    print(f"📁 Found database at: {db_path}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📋 Tables in database:")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will delete ALL data from trips and alerts tables!")
    confirm = input("Type 'yes' to continue: ")
    
    if confirm.lower() != 'yes':
        print("❌ Operation cancelled.")
        conn.close()
        return
    
    # Delete data from tables
    print("\n🗑️  Clearing data from tables...")
    
    try:
        # Clear trips table
        cursor.execute("DELETE FROM trips")
        trips_deleted = cursor.rowcount
        print(f"   ✅ Deleted {trips_deleted} trips")
        
        # Clear alerts table
        cursor.execute("DELETE FROM alerts")
        alerts_deleted = cursor.rowcount
        print(f"   ✅ Deleted {alerts_deleted} alerts")
        
        # Reset auto-increment counters
        print("\n🔄 Resetting auto-increment counters...")
        
        # Reset trips sequence
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='trips'")
        print(f"   ✅ Reset trips ID counter")
        
        # Reset alerts sequence
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='alerts'")
        print(f"   ✅ Reset alerts ID counter")
        
        # Commit changes
        conn.commit()
        
        print("\n✅ Database cleaned successfully!")
        print("\n📊 Next IDs will start from:")
        print("   - Trips: 1")
        print("   - Alerts: 1")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("🧹 DATABASE CLEANER")
    print("=" * 50)
    clean_database()
    print("\n" + "=" * 50)