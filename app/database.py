import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATA_DIR = os.path.join(os.getcwd(), "data")

DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'driversafety.db')}"

# DEBUG
print("=" * 50)
print(f"DATABASE_URL = {DATABASE_URL}")
print(f"DATA_DIR = {DATA_DIR}")
print("=" * 50)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()