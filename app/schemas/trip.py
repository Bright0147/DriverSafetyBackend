from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# ========== PYDANTIC MODELS (Request/Response) ==========

class TripCreate(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    distance_km: float
    safety_score: int
    # ========== ADD THESE FIELDS ==========
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    start_latitude: Optional[float] = None
    start_longitude: Optional[float] = None
    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    max_speed: Optional[float] = None
    avg_speed: Optional[float] = None
    drowsiness_count: Optional[int] = 0
    distraction_count: Optional[int] = 0
    seatbelt_violations: Optional[int] = 0
    fatigue_count: Optional[int] = 0

class TripResponse(BaseModel):
    id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    distance_km: float
    safety_score: int
    created_at: datetime
    # ========== ADD THESE FIELDS ==========
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    start_latitude: Optional[float] = None
    start_longitude: Optional[float] = None
    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    max_speed: Optional[float] = None
    avg_speed: Optional[float] = None
    drowsiness_count: Optional[int] = 0
    distraction_count: Optional[int] = 0
    seatbelt_violations: Optional[int] = 0
    fatigue_count: Optional[int] = 0
    message: Optional[str] = None

class TripUpdate(BaseModel):
    end_time: Optional[datetime] = None
    end_location: Optional[str] = None
    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    distance_km: Optional[float] = None
    duration_minutes: Optional[int] = None
    safety_score: Optional[int] = None
    max_speed: Optional[float] = None
    avg_speed: Optional[float] = None

# ========== SQLALCHEMY DATABASE MODEL ==========

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=0)
    distance_km = Column(Float, default=0.0)
    safety_score = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # ========== ADD THESE COLUMNS ==========
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

# ========== API ENDPOINTS ==========

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/v1/trips", tags=["trips"])

@router.post("/", response_model=TripResponse)
async def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    """Create a new trip"""
    try:
        db_trip = Trip(
            user_id=trip.user_id,
            start_time=trip.start_time,
            end_time=trip.end_time,
            duration_minutes=trip.duration_minutes,
            distance_km=trip.distance_km,
            safety_score=trip.safety_score,
            # New fields
            start_location=trip.start_location,
            end_location=trip.end_location,
            start_latitude=trip.start_latitude,
            start_longitude=trip.start_longitude,
            end_latitude=trip.end_latitude,
            end_longitude=trip.end_longitude,
            max_speed=trip.max_speed,
            avg_speed=trip.avg_speed,
            drowsiness_count=trip.drowsiness_count,
            distraction_count=trip.distraction_count,
            seatbelt_violations=trip.seatbelt_violations,
            fatigue_count=trip.fatigue_count
        )
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        
        return TripResponse(
            id=db_trip.id,
            user_id=db_trip.user_id,
            start_time=db_trip.start_time,
            end_time=db_trip.end_time,
            duration_minutes=db_trip.duration_minutes,
            distance_km=db_trip.distance_km,
            safety_score=db_trip.safety_score,
            created_at=db_trip.created_at,
            start_location=db_trip.start_location,
            end_location=db_trip.end_location,
            start_latitude=db_trip.start_latitude,
            start_longitude=db_trip.start_longitude,
            end_latitude=db_trip.end_latitude,
            end_longitude=db_trip.end_longitude,
            max_speed=db_trip.max_speed,
            avg_speed=db_trip.avg_speed,
            drowsiness_count=db_trip.drowsiness_count,
            distraction_count=db_trip.distraction_count,
            seatbelt_violations=db_trip.seatbelt_violations,
            fatigue_count=db_trip.fatigue_count,
            message="Trip created successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[TripResponse])
async def get_trips(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get all trips, optionally filtered by user_id"""
    query = db.query(Trip)
    
    if user_id:
        query = query.filter(Trip.user_id == user_id)
    
    trips = query.order_by(Trip.start_time.desc()).offset(offset).limit(limit).all()
    
    return [
        TripResponse(
            id=trip.id,
            user_id=trip.user_id,
            start_time=trip.start_time,
            end_time=trip.end_time,
            duration_minutes=trip.duration_minutes,
            distance_km=trip.distance_km,
            safety_score=trip.safety_score,
            created_at=trip.created_at,
            start_location=trip.start_location,
            end_location=trip.end_location,
            start_latitude=trip.start_latitude,
            start_longitude=trip.start_longitude,
            end_latitude=trip.end_latitude,
            end_longitude=trip.end_longitude,
            max_speed=trip.max_speed,
            avg_speed=trip.avg_speed,
            drowsiness_count=trip.drowsiness_count,
            distraction_count=trip.distraction_count,
            seatbelt_violations=trip.seatbelt_violations,
            fatigue_count=trip.fatigue_count
        )
        for trip in trips
    ]

@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """Get a specific trip by ID"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return TripResponse(
        id=trip.id,
        user_id=trip.user_id,
        start_time=trip.start_time,
        end_time=trip.end_time,
        duration_minutes=trip.duration_minutes,
        distance_km=trip.distance_km,
        safety_score=trip.safety_score,
        created_at=trip.created_at,
        start_location=trip.start_location,
        end_location=trip.end_location,
        start_latitude=trip.start_latitude,
        start_longitude=trip.start_longitude,
        end_latitude=trip.end_latitude,
        end_longitude=trip.end_longitude,
        max_speed=trip.max_speed,
        avg_speed=trip.avg_speed,
        drowsiness_count=trip.drowsiness_count,
        distraction_count=trip.distraction_count,
        seatbelt_violations=trip.seatbelt_violations,
        fatigue_count=trip.fatigue_count
    )

@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(trip_id: int, trip_update: TripUpdate, db: Session = Depends(get_db)):
    """Update a trip (e.g., when trip ends)"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    update_data = trip_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(trip, field, value)
    
    db.commit()
    db.refresh(trip)
    
    return TripResponse(
        id=trip.id,
        user_id=trip.user_id,
        start_time=trip.start_time,
        end_time=trip.end_time,
        duration_minutes=trip.duration_minutes,
        distance_km=trip.distance_km,
        safety_score=trip.safety_score,
        created_at=trip.created_at,
        start_location=trip.start_location,
        end_location=trip.end_location,
        start_latitude=trip.start_latitude,
        start_longitude=trip.start_longitude,
        end_latitude=trip.end_latitude,
        end_longitude=trip.end_longitude,
        max_speed=trip.max_speed,
        avg_speed=trip.avg_speed,
        drowsiness_count=trip.drowsiness_count,
        distraction_count=trip.distraction_count,
        seatbelt_violations=trip.seatbelt_violations,
        fatigue_count=trip.fatigue_count,
        message="Trip updated successfully"
    )

@router.delete("/{trip_id}")
async def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Delete a trip"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(trip)
    db.commit()
    
    return {"message": "Trip deleted successfully", "trip_id": trip_id}