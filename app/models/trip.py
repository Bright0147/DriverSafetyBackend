from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    distance_km = Column(Float)
    safety_score = Column(Integer)
    
    # ========== ADD THESE MISSING FIELDS ==========
    start_location = Column(String, nullable=True)
    end_location = Column(String, nullable=True)
    start_latitude = Column(Float, nullable=True)
    start_longitude = Column(Float, nullable=True)
    end_latitude = Column(Float, nullable=True)
    end_longitude = Column(Float, nullable=True)
    max_speed = Column(Float, nullable=True)
    avg_speed = Column(Float, nullable=True)
    drowsiness_count = Column(Integer, default=0)
    distraction_count = Column(Integer, default=0)
    seatbelt_violations = Column(Integer, default=0)
    fatigue_count = Column(Integer, default=0)
    completed = Column(Integer, default=0)  # 0 = false, 1 = true
    synced = Column(Integer, default=0)      # 0 = false, 1 = true
    # ===========================================
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="trips")
    alerts = relationship("Alert", back_populates="trip", cascade="all, delete-orphan")