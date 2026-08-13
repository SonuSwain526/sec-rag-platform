# from app.core.security import hash_password, verify_password
# h = hash_password('testpass123')
# print('Hash:', h)
# print('Verify correct:', verify_password('testpass123', h))
# print('Verify wrong:', verify_password('wrongpass', h))
# from app.db.session import SessionLocal
# from app.models.user import User
# db = SessionLocal()
# user = db.query(User).filter(User.email == 'sy@example.com').first()
# print('Email:', user.email)
# print('Hashed password:', user.hashed_password)
# db.close()

from app.core.security import verify_password
from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.email == 'sy@example.com').first()
print('Stored hash:', user.hashed_password)
print('Verify with password=string:', verify_password('string', user.hashed_password))
db.close()