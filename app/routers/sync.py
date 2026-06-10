from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Trip, Alert
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

class SyncTrip(BaseModel):
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    distance_km: float
    safety_score: int
    alerts: List[dict] = []

@router.post("/batch")
async def batch_sync(sync_data: List[SyncTrip], db: Session = Depends(get_db)):
    trips_synced = 0
    alerts_synced = 0
    
    for trip_data in sync_data:
        # Create trip
        db_trip = Trip(
            start_time=trip_data.start_time,
            end_time=trip_data.end_time,
            duration_minutes=trip_data.duration_minutes,
            distance_km=trip_data.distance_km,
            safety_score=trip_data.safety_score
        )
        db.add(db_trip)
        db.flush()
        
        # Create alerts for this trip
        for alert_data in trip_data.alerts:
            db_alert = Alert(
                trip_id=db_trip.id,
                alert_type=alert_data.get("alert_type"),
                severity=alert_data.get("severity"),
                timestamp=datetime.fromisoformat(alert_data.get("timestamp"))
            )
            db.add(db_alert)
            alerts_synced += 1
        
        trips_synced += 1
    
    db.commit()
    return {"message": f"Synced {trips_synced} trips and {alerts_synced} alerts"}
