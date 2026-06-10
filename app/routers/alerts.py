# app/routers/alerts.py - CLEAN VERSION (NO DUPLICATE ROUTES)
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Alert
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])

class AlertCreate(BaseModel):
    user_id: int
    trip_id: Optional[int] = None
    alert_type: str
    severity: str
    timestamp: datetime
    message: Optional[str] = None

# ============================================
# CREATE ALERTS - ONLY ONE ROUTE
# ============================================
@router.post("", response_model=dict)  # ← NO trailing slash
async def create_alerts(alerts: List[AlertCreate], db: Session = Depends(get_db)):
    """Create multiple alerts"""
    
    created_count = 0
    
    for alert_data in alerts:
        new_alert = Alert(
            user_id=alert_data.user_id,
            trip_id=alert_data.trip_id,
            alert_type=alert_data.alert_type,
            severity=alert_data.severity,
            timestamp=alert_data.timestamp,
            acknowledged=False
        )
        db.add(new_alert)
        created_count += 1
    
    db.commit()
    return {"message": f"{created_count} alerts saved", "success": True}

# ============================================
# GET ALL ALERTS - ONLY ONE ROUTE
# ============================================
@router.get("", response_model=List[dict])  # ← NO trailing slash
async def get_alerts(
    user_id: Optional[int] = Query(None),
    trip_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all alerts - filter by user_id or trip_id"""
    
    query = db.query(Alert)
    
    if user_id:
        query = query.filter(Alert.user_id == user_id)
    if trip_id:
        query = query.filter(Alert.trip_id == trip_id)
    
    alerts = query.order_by(Alert.timestamp.desc()).all()
    
    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "trip_id": a.trip_id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "timestamp": a.timestamp,
            "acknowledged": a.acknowledged
        }
        for a in alerts
    ]