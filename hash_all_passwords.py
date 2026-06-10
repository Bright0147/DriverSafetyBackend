# hash_all_passwords.py
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def hash_all_passwords():
    conn = sqlite3.connect('data/driversafety.db')
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT id, username, hashed_password FROM users")
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users to process\n")
    
    updated = 0
    for user_id, username, current_pw in users:
        # Check if password is already hashed (starts with $2b$)
        if not current_pw.startswith('$2b$'):
            # Hash the plain text password
            hashed = hash_password(current_pw)
            cursor.execute("UPDATE users SET hashed_password = ? WHERE id = ?", (hashed, user_id))
            print(f"✅ Updated: {username} (ID: {user_id})")
            updated += 1
        else:
            print(f"⚠️ Already hashed: {username} (ID: {user_id})")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} passwords to bcrypt hash format")
    print("\n📋 Test login with: admin@driversafety.com / admin123")

if __name__ == "__main__":
    hash_all_passwords()