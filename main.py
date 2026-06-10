from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine, Base, SessionLocal
from app.models import User, Trip, Alert
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Driver Safety API", version="1.0.0")

# CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to parse datetime strings
def parse_datetime(date_string):
    if not date_string:
        return None
    try:
        date_string = date_string.replace('Z', '+00:00')
        return datetime.fromisoformat(date_string)
    except Exception as e:
        print(f"Date parsing error: {e}")
        return None

@app.get("/")
async def root():
    return {"message": "Driver Safety API is running"}

@app.post("/api/v1/alerts")
async def create_alerts(request: Request):
    db = SessionLocal()
    
    try:
        data = await request.json()
        print(f"Received data type: {type(data)}")
        print(f"Data: {data}")
        
        # Handle both formats
        if isinstance(data, list):
            alerts = data
        elif isinstance(data, dict) and "alerts" in data:
            alerts = data["alerts"]
        else:
            alerts = []
        
        print(f"Processing {len(alerts)} alerts")
        
        created_count = 0
        for alert_data in alerts:
            timestamp = parse_datetime(alert_data.get("timestamp"))
            
            print(f"Creating alert with type: {alert_data.get('alert_type')}")
            
            new_alert = Alert(
                trip_id=alert_data.get("trip_id"),
                alert_alert_type=alert_data.get("alert_type"),
                severity=alert_data.get("severity"),
                timestamp=timestamp
            )
            db.add(new_alert)
            created_count += 1
        
        db.commit()
        db.close()
        return {"message": f"{created_count} alerts saved", "success": True}
        
    except Exception as e:
        db.rollback()
        db.close()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "success": False}
        )

@app.get("/api/v1/alerts")
async def get_alerts():
    db = SessionLocal()
    alerts = db.query(Alert).all()
    db.close()
    return [
        {
            "id": a.id,
            "trip_id": a.trip_id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "timestamp": a.timestamp
        }
        for a in alerts
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
