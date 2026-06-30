from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Driver specific fields
    driver_license = Column(String)
    phone_number = Column(String)
    vehicle_id = Column(String)

    # ROLE MANAGEMENT - IMPORTANT
    role = Column(String, default="driver")  # "admin" or "driver"
    status = Column(String, default="active")  # "active", "inactive", "suspended"
    synced = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships (matches Android Room relationships)
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
