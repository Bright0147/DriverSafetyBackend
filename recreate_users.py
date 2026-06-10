# recreate_users.py
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def recreate_users():
    conn = sqlite3.connect('data/driversafety.db')
    cursor = conn.cursor()
    
    # Delete existing users
    cursor.execute("DELETE FROM users")
    print("🗑️ Removed existing users")
    
    # Create admin with hashed password
    admin_hash = hash_password("admin123")
    cursor.execute('''
        INSERT INTO users (username, full_name, email, hashed_password, is_admin, role, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ("admin", "Administrator", "admin@driversafety.com", admin_hash, 1, "admin", "active"))
    print("✅ Admin user created (password hashed)")
    
    # Create driver with hashed password
    driver_hash = hash_password("driver123")
    cursor.execute('''
        INSERT INTO users (username, full_name, email, hashed_password, is_admin, role, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ("driver", "Driver User", "driver@driversafety.com", driver_hash, 0, "driver", "active"))
    print("✅ Driver user created (password hashed)")
    
    # Verify
    cursor.execute("SELECT id, username, hashed_password FROM users")
    users = cursor.fetchall()
    print("\n📋 Users in database:")
    for user in users:
        print(f"   ID: {user[0]}, Username: {user[1]}, Hashed: {user[2][:20]}...")
    
    conn.commit()
    conn.close()
    print("\n✅ Users recreated with hashed passwords!")

if __name__ == "__main__":
    recreate_users()