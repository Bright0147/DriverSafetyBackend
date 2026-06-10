from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()
admin = db.query(User).filter(User.username == 'admin').first()

if admin:
    admin.role = 'admin'
    admin.is_admin = True
    admin.status = 'active'
    db.commit()
    print(f'✅ Admin updated successfully!')
    print(f'   Username: {admin.username}')
    print(f'   Role: {admin.role}')
    print(f'   Is Admin: {admin.is_admin}')
    print(f'   Status: {admin.status}')
else:
    print('Admin not found - creating new admin')
    from app.utils.password import hash_password
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
    print('✅ Admin created!')

db.close()
