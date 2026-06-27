import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from environment (for Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL doesn't exist, use SQLite for local development
if not DATABASE_URL:
    DATA_DIR = os.path.join(os.getcwd(), "data")
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'driversafety.db')}"
    
    # DEBUG for local
    print("=" * 50)
    print(f"LOCAL DEVELOPMENT MODE")
    print(f"DATABASE_URL = {DATABASE_URL}")
    print(f"DATA_DIR = {DATA_DIR}")
    print("=" * 50)
    
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL on Render
    print("=" * 50)
    print(f"PRODUCTION MODE - Using PostgreSQL")
    print("=" * 50)
    
    # Handle Render's postgres:// vs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # PostgreSQL configuration (no check_same_thread)
    engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create tables (useful for startup)
def create_tables():
    Base.metadata.create_all(bind=engine)