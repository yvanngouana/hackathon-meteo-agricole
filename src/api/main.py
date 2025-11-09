"""
API FastAPI pour la plateforme météo agricole
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Configuration
app = FastAPI(
    title="API Météo Agricole",
    description="API pour prévisions météo et recommandations agricoles",
    version="0.1.0"
)

# CORS pour frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the models router
from .routers import models
app.include_router(models.router)

# Connexion à la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/meteo_agricole")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèles Pydantic
class FieldCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    crop_type: Optional[str] = None
    area_hectares: Optional[float] = None


class WeatherResponse(BaseModel):
    temperature_celsius: float
    humidity_percent: float
    weather_description: str
    timestamp: datetime


class ForecastResponse(BaseModel):
    forecast_date: datetime
    temp_min: float
    temp_max: float
    rain_mm: float
    irrigation_need_mm: Optional[float] = None
    disease_risk: Optional[str] = None


class IrrigationRecommendation(BaseModel):
    date: datetime
    irrigation_needed: bool
    water_amount_mm: float
    reason: str


# Routes
@app.get("/")
async def root():
    """Route racine"""
    return {
        "message": "Bienvenue sur l'API Météo Agricole",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check pour monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/fields", status_code=201)
async def create_field(field: FieldCreate, db: SessionLocal = Depends(get_db)):
    """
    Créer un nouveau champ agricole
    """
    try:
        from etl.load import DatabaseLoader, AgriculturalField

        loader = DatabaseLoader()
        field_id = loader.create_field(
            name=field.name,
            latitude=field.latitude,
            longitude=field.longitude,
            crop_type=field.crop_type,
            area_hectares=field.area_hectares
        )

        return {
            "id": field_id,
            "message": "Champ créé avec succès",
            "field": field.dict()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/weather/current", response_model=WeatherResponse)
async def get_current_weather(latitude: float, longitude: float, db: SessionLocal = Depends(get_db)):
    """
    Obtenir la météo actuelle pour une localisation depuis la base de données
    """
    try:
        query = text("""
            SELECT * FROM weather_records
            WHERE latitude = :lat AND longitude = :lon
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        result = db.execute(query, {"lat": latitude, "lon": longitude}).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Aucune donnée météo trouvée pour cette localisation.")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/weather/forecast", response_model=List[ForecastResponse])
async def get_weather_forecast(latitude: float, longitude: float, days: int = 7, db: SessionLocal = Depends(get_db)):
    """
    Obtenir les prévisions météo depuis la base de données
    """
    try:
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days)

        query = text("""
            SELECT * FROM weather_forecasts
            WHERE latitude = :lat AND longitude = :lon
            AND forecast_date >= :start_date AND forecast_date < :end_date
            ORDER BY forecast_date ASC
        """)
        results = db.execute(query, {
            "lat": latitude,
            "lon": longitude,
            "start_date": start_date,
            "end_date": end_date
        }).fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="Aucune prévision trouvée pour cette période.")

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/predictions/irrigation", response_model=List[IrrigationRecommendation])
async def get_irrigation_recommendations(latitude: float, longitude: float, days: int = 7, db: SessionLocal = Depends(get_db)):
    """
    Obtenir les recommandations d'irrigation depuis la base de données
    """
    try:
        forecasts = await get_weather_forecast(latitude, longitude, days, db)
        
        recommendations = []
        for forecast in forecasts:
            irrigation_need = forecast.irrigation_need_mm or 0

            if irrigation_need > 5:
                recommendation = {
                    "date": forecast.forecast_date,
                    "irrigation_needed": True,
                    "water_amount_mm": round(irrigation_need, 2),
                    "reason": f"Besoin en eau estimé: {irrigation_need:.1f}mm (ET0 - pluie)"
                }
            else:
                recommendation = {
                    "date": forecast.forecast_date,
                    "irrigation_needed": False,
                    "water_amount_mm": 0,
                    "reason": "Pluie suffisante ou faible évapotranspiration"
                }
            recommendations.append(recommendation)

        return recommendations

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/predictions/disease-risk")
async def get_disease_risk(latitude: float, longitude: float, days: int = 7, db: SessionLocal = Depends(get_db)):
    """
    Obtenir les risques de maladies agricoles depuis la base de données
    """
    try:
        forecasts = await get_weather_forecast(latitude, longitude, days, db)

        disease_alerts = []
        for forecast in forecasts:
            risk_level = forecast.disease_risk or 'low'

            if risk_level == 'high':
                alert = {
                    "date": forecast.forecast_date,
                    "risk_level": risk_level,
                    "humidity": forecast.humidity,
                    "temperature": forecast.temp_day,
                    "recommendation": "Risque élevé de maladies fongiques. Surveiller les cultures."
                }
                disease_alerts.append(alert)
            elif risk_level == 'medium':
                alert = {
                    "date": forecast.forecast_date,
                    "risk_level": risk_level,
                    "humidity": forecast.humidity,
                    "temperature": forecast.temp_day,
                    "recommendation": "Risque modéré. Inspection recommandée."
                }
                disease_alerts.append(alert)

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "alerts": disease_alerts,
            "alert_count": len(disease_alerts)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
