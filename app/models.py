from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    phone_number = Column(String, nullable=True)
    driver_license = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    distance_km = Column(Float)
    safety_score = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # ← ADD THIS or make nullable
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    alert_type = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime(timezone=True))
    acknowledged = Column(Boolean, default=False)  # ← You also have this field
    created_at = Column(DateTime(timezone=True), server_default=func.now())