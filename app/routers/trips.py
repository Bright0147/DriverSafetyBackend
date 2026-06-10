# app/routers/trips.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Trip
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

router = APIRouter(prefix="/api/v1/trips", tags=["trips"])

class TripCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    distance_km: float
    safety_score: int
    user_id: int
    start_location: Optional[str] = None  # ← ADD THIS
    end_location: Optional[str] = None    # ← ADD THIS

@router.post("")
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
            start_location=trip.start_location,  # ← ADD THIS
            end_location=trip.end_location       # ← ADD THIS
        )
        
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        
        return {
            "id": db_trip.id,
            "user_id": db_trip.user_id,
            "start_time": db_trip.start_time,
            "end_time": db_trip.end_time,
            "duration_minutes": db_trip.duration_minutes,
            "distance_km": db_trip.distance_km,
            "safety_score": db_trip.safety_score,
            "start_location": db_trip.start_location,  # ← ADD THIS
            "end_location": db_trip.end_location,      # ← ADD THIS
            "message": "Trip created successfully"
        }
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return {"error": str(e)}, 500

@router.get("")
async def get_trips(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all trips - optionally filter by user_id"""
    query = db.query(Trip)
    if user_id:
        query = query.filter(Trip.user_id == user_id)
    trips = query.order_by(Trip.start_time.desc()).all()
    
    return [
        {
            "id": trip.id,
            "user_id": trip.user_id,
            "start_time": trip.start_time,
            "end_time": trip.end_time,
            "duration_minutes": trip.duration_minutes,
            "distance_km": trip.distance_km,
            "safety_score": trip.safety_score,
            "start_location": trip.start_location,  # ← ADD THIS
            "end_location": trip.end_location,      # ← ADD THIS
            "created_at": trip.created_at
        }
        for trip in trips
    ]