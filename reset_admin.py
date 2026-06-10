from app.database import SessionLocal
from app.models.user import User
from app.utils.password import hash_password

db = SessionLocal()

# Find admin user
admin = db.query(User).filter(User.username == 'admin').first()

if admin:
    print(f'Found admin: {admin.username}')
    admin.hashed_password = hash_password('admin123')
    admin.role = 'admin'
    admin.is_admin = True
    db.commit()
    print('✅ Admin password reset and role assigned')
    print(f'   Username: {admin.username}')
    print(f'   Role: {admin.role}')
    print(f'   Is Admin: {admin.is_admin}')
else:
    print('Admin not found, creating new admin')
    admin = User(
        username='admin',
        email='admin@driversafety.com',
        full_name='System Administrator',
        hashed_password=hash_password('admin123'),
        role='admin',
        is_admin=True,
        status='active'
    )
    db.add(admin)
    db.commit()
    print('✅ Admin created')

db.close()
