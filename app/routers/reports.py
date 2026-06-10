from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Trip, Alert, User

router = APIRouter()

@router.get("/summary")
async def get_summary(db: Session = Depends(get_db)):
    total_trips = db.query(Trip).count()
    total_alerts = db.query(Alert).count()
    avg_safety_score = db.query(func.avg(Trip.safety_score)).scalar() or 0
    
    return {
        "total_trips": total_trips,
        "total_alerts": total_alerts,
        "average_safety_score": avg_safety_score
    }

@router.get("/top-violators")
async def get_top_violators(db: Session = Depends(get_db)):
    # This is a placeholder - implement based on your needs
    return []