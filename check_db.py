# check_db.py
from app.database import engine
from sqlalchemy import inspect, text

print("=== CHECKING DATABASE ===")

# 1. Check columns in trips table
inspector = inspect(engine)
columns = inspector.get_columns('trips')
print("\n=== COLUMNS IN TRIPS TABLE ===")
for col in columns:
    print(f"  {col['name']} ({col['type']})")

# 2. Check total trips
from sqlalchemy.orm import Session
from app.models.trip import Trip
db = Session(engine)
trips = db.query(Trip).all()
print(f"\n=== TOTAL TRIPS: {len(trips)} ===")

for trip in trips[:3]:
    print(f"  Trip ID: {trip.id}, User ID: {trip.user_id}")

# 3. Check if location columns exist
print("\n=== CHECKING FOR LOCATION COLUMNS ===")
col_names = [col['name'] for col in columns]
if 'start_location' in col_names:
    print("  ✅ start_location EXISTS")
else:
    print("  ❌ start_location MISSING")

if 'end_location' in col_names:
    print("  ✅ end_location EXISTS")
else:
    print("  ❌ end_location MISSING")

db.close()
print("\n=== DONE ===")