from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.trip import Trip
from app.models.alert import Alert

# Import routers
from app.routers import auth
from app.routers import users
from app.routers import trips

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Driver Safety API",
    version="1.0.0"
)

# Register routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(trips.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_datetime(date_string):
    if not date_string:
        return None
    try:
        date_string = date_string.replace("Z", "+00:00")
        return datetime.fromisoformat(date_string)
    except Exception as e:
        print(f"Date parsing error: {e}")
        return None

@app.get("/")
async def root():
    return {"message": "Driver Safety API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ============================================================
# REMOVED THE REDIRECT - NO MORE LOOP!
# ============================================================

# ============================================================
# ALERTS ENDPOINTS
# ============================================================

@app.post("/api/v1/alerts")
async def create_alerts(request: Request):
    db = SessionLocal()
    try:
        data = await request.json()
        
        if isinstance(data, list):
            alerts = data
        elif isinstance(data, dict) and "alerts" in data:
            alerts = data["alerts"]
        else:
            alerts = []
        
        created_count = 0
        for alert_data in alerts:
            timestamp = parse_datetime(alert_data.get("timestamp"))
            
            # FIX: Add user_id
            new_alert = Alert(
                user_id=alert_data.get("user_id"),  # ← ADD THIS LINE
                trip_id=alert_data.get("trip_id"),
                alert_type=alert_data.get("alert_type"),
                severity=alert_data.get("severity"),
                timestamp=timestamp
            )
            db.add(new_alert)
            created_count += 1
        
        db.commit()
        return {"message": f"{created_count} alerts saved", "success": True}
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "success": False}
        )
    finally:
        db.close()

@app.get("/api/v1/alerts")
async def get_alerts():
    db = SessionLocal()
    try:
        alerts = db.query(Alert).all()
        return [
            {
                "id": a.id,
                "user_id": a.user_id,  # ← ADD THIS
                "trip_id": a.trip_id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "timestamp": a.timestamp
            }
            for a in alerts
        ]
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )