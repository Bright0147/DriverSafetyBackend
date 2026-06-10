# add_columns_to_trips.py
from app.database import engine
from sqlalchemy import text

print("Adding missing columns to trips table...")

with engine.connect() as conn:
    # List of columns to add
    columns_to_add = [
        ("start_location", "VARCHAR"),
        ("end_location", "VARCHAR"),
        ("start_latitude", "FLOAT"),
        ("start_longitude", "FLOAT"),
        ("end_latitude", "FLOAT"),
        ("end_longitude", "FLOAT"),
        ("max_speed", "FLOAT"),
        ("avg_speed", "FLOAT"),
        ("drowsiness_count", "INTEGER DEFAULT 0"),
        ("distraction_count", "INTEGER DEFAULT 0"),
        ("seatbelt_violations", "INTEGER DEFAULT 0"),
        ("fatigue_count", "INTEGER DEFAULT 0"),
        ("completed", "INTEGER DEFAULT 0"),
        ("synced", "INTEGER DEFAULT 0"),
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            conn.execute(text(f"ALTER TABLE trips ADD COLUMN {col_name} {col_type}"))
            print(f"✅ Added column: {col_name}")
        except Exception as e:
            if "duplicate column" in str(e).lower():
                print(f"⚠️ Column already exists: {col_name}")
            else:
                print(f"❌ Error adding {col_name}: {e}")
    
    conn.commit()

print("\n✅ All columns added successfully!")