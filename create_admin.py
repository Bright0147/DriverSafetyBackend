# create_admin.py
import sqlite3
import hashlib

def create_admin():
    # Database path
    db_path = "data/driversafety.db"
    
    # Admin details
    username = "admin"
    email = "admin@driversafety.com"
    password = "admin123"
    full_name = "System Administrator"
    is_admin = True
    
    # Hash password (using simple hash - adjust based on your backend's hashing)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if admin already exists
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    existing = cursor.fetchone()
    
    if existing:
        print(f"⚠️ User already exists: {existing}")
        confirm = input("Do you want to update the password? (yes/no): ")
        if confirm.lower() == 'yes':
            cursor.execute("UPDATE users SET hashed_password = ? WHERE username = ?", (hashed_password, username))
            conn.commit()
            print("✅ Admin password updated!")
    else:
        # Insert admin user
        cursor.execute("""
            INSERT INTO users (
                username, email, hashed_password, full_name, is_admin, 
                is_active, role, status, created_at, synced
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), 1)
        """, (username, email, hashed_password, full_name, is_admin, 1, "admin", "active"))
        
        conn.commit()
        print(f"✅ Admin user created!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   User ID: {cursor.lastrowid}")
    
    conn.close()

if __name__ == "__main__":
    print("=" * 40)
    print("👑 ADMIN CREATOR")
    print("=" * 40)
    create_admin()