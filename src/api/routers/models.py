"""
Routes pour les modèles ML
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import pandas as pd

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.etl.extract import WeatherDataExtractor
from src.etl.transform import WeatherDataTransformer

# Importer les modèles ML
from src.models.rain_prediction import RainPredictionModel
from src.models.drought_detection import DroughtDetectionModel
from src.models.disease_risk import DiseaseRiskModel

router = APIRouter(prefix="/api/models", tags=["models"])

# Modèles Pydantic
class PredictionRequest(BaseModel):
    latitude: float
    longitude: float
    days: int = 7

class RainPrediction(BaseModel):
    date: str
    predicted_rain_mm: float
    confidence: float

class DroughtPrediction(BaseModel):
    date: str
    is_drought: bool
    drought_probability: float
    drought_level: str

class DiseasePrediction(BaseModel):
    date: str
    disease_risk_level: str
    risk_probability: float
    risk_factors: dict

class RainPredictionResponse(BaseModel):
    location: dict
    predictions: List[RainPrediction]
    period_days: int

class DroughtPredictionResponse(BaseModel):
    location: dict
    predictions: List[DroughtPrediction]
    period_days: int

class DiseasePredictionResponse(BaseModel):
    location: dict
    predictions: List[DiseasePrediction]
    period_days: int

@router.get("/rain-prediction")
async def get_rain_prediction(request: PredictionRequest = Depends()):
    """
    Endpoint pour prédire la pluie future
    """
    try:
        # Créer une instance du modèle
        model = RainPredictionModel()
        
        # Créer des données basiques pour entraîner le modèle rapidement
        # Dans un vrai environnement, on aurait des données historiques
        from src.models.rain_prediction import create_sample_data
        sample_data = create_sample_data()
        
        # Entraîner le modèle avec les données d'exemple (pour la démo)
        try:
            model.train(sample_data)
        except:
            # Si entraînement échoue, on continue avec le modèle vide
            pass
        
        # Récupérer les prévisions météo
        extractor = WeatherDataExtractor()
        transformer = WeatherDataTransformer()
        
        raw_forecasts = extractor.get_forecast(request.latitude, request.longitude, request.days)
        df = transformer.transform_forecast(raw_forecasts)
        df_enriched = transformer.calculate_derived_features(df)
        
        # Convertir en format approprié pour la prédiction
        future_data = df_enriched.to_dict(orient='records')
        
        # Faire la prédiction
        predictions = model.predict(future_data)
        
        return RainPredictionResponse(
            location={"latitude": request.latitude, "longitude": request.longitude},
            predictions=predictions,
            period_days=request.days
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction de pluie: {str(e)}")

@router.get("/drought-prediction")
async def get_drought_prediction(request: PredictionRequest = Depends()):
    """
    Endpoint pour prédire les risques de sécheresse
    """
    try:
        # Créer une instance du modèle
        model = DroughtDetectionModel()
        
        # Créer des données basiques pour entraîner le modèle rapidement
        from src.models.drought_detection import create_sample_data
        sample_data = create_sample_data()
        
        # Entraîner le modèle avec les données d'exemple (pour la démo)
        try:
            model.train(sample_data)
        except:
            # Si entraînement échoue, on continue avec le modèle vide
            pass
        
        # Récupérer les prévisions météo
        extractor = WeatherDataExtractor()
        transformer = WeatherDataTransformer()
        
        raw_forecasts = extractor.get_forecast(request.latitude, request.longitude, request.days)
        df = transformer.transform_forecast(raw_forecasts)
        df_enriched = transformer.calculate_derived_features(df)
        
        # Convertir en format approprié pour la prédiction
        future_data = df_enriched.to_dict(orient='records')
        
        # Faire la prédiction
        predictions = model.predict(future_data)
        
        return DroughtPredictionResponse(
            location={"latitude": request.latitude, "longitude": request.longitude},
            predictions=predictions,
            period_days=request.days
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction de sécheresse: {str(e)}")

@router.get("/disease-risk")
async def get_disease_risk(request: PredictionRequest = Depends()):
    """
    Endpoint pour prédire les risques de maladies agricoles
    """
    try:
        # Créer une instance du modèle
        model = DiseaseRiskModel()
        
        # Créer des données basiques pour entraîner le modèle rapidement
        from src.models.disease_risk import create_sample_data
        sample_data = create_sample_data()
        
        # Entraîner le modèle avec les données d'exemple (pour la démo)
        try:
            model.train(sample_data)
        except:
            # Si entraînement échoue, on continue avec le modèle vide
            pass
        
        # Récupérer les prévisions météo
        extractor = WeatherDataExtractor()
        transformer = WeatherDataTransformer()
        
        raw_forecasts = extractor.get_forecast(request.latitude, request.longitude, request.days)
        df = transformer.transform_forecast(raw_forecasts)
        df_enriched = transformer.calculate_derived_features(df)
        
        # Convertir en format approprié pour la prédiction
        future_data = df_enriched.to_dict(orient='records')
        
        # Faire la prédiction
        predictions = model.predict(future_data)
        
        return DiseasePredictionResponse(
            location={"latitude": request.latitude, "longitude": request.longitude},
            predictions=predictions,
            period_days=request.days
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction de risque de maladies: {str(e)}")