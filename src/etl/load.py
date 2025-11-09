"""
Module de chargement des données dans PostgreSQL/TimescaleDB
"""

import os
from datetime import datetime
from typing import Dict, List
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


# Modèles de données
class WeatherRecord(Base):
    """Table pour les enregistrements météo"""
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature_celsius = Column(Float)
    feels_like_celsius = Column(Float)
    humidity_percent = Column(Float)
    pressure_hpa = Column(Float)
    wind_speed_ms = Column(Float)
    clouds_percent = Column(Float)
    uvi = Column(Float)
    weather_description = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class WeatherForecast(Base):
    """Table pour les prévisions météo"""
    __tablename__ = "weather_forecasts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    forecast_date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temp_min = Column(Float)
    temp_max = Column(Float)
    temp_day = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)
    rain_mm = Column(Float)
    pop = Column(Float)  # Probabilité de pluie
    uvi = Column(Float)
    # Features dérivées
    temp_amplitude = Column(Float)
    water_stress_index = Column(Float)
    et0_mm = Column(Float)
    irrigation_need_mm = Column(Float)
    disease_risk = Column(String)


class AgriculturalField(Base):
    """Table pour les champs agricoles"""
    __tablename__ = "agricultural_fields"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    crop_type = Column(String)
    area_hectares = Column(Float)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)


class DatabaseLoader:
    """Gestionnaire de chargement des données dans PostgreSQL"""

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/meteo_agricole")
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)

        # Créer les tables si elles n'existent pas
        Base.metadata.create_all(self.engine)
        logger.info("Connexion à la base de données établie")

    def load_current_weather(self, weather_data: Dict, latitude: float, longitude: float) -> int:
        """
        Charge les données météo actuelles

        Args:
            weather_data: Données météo transformées
            latitude: Latitude
            longitude: Longitude

        Returns:
            ID de l'enregistrement créé
        """
        try:
            session = self.Session()

            record = WeatherRecord(
                timestamp=weather_data.get("timestamp", datetime.now()),
                latitude=latitude,
                longitude=longitude,
                temperature_celsius=weather_data.get("temperature_celsius"),
                feels_like_celsius=weather_data.get("feels_like_celsius"),
                humidity_percent=weather_data.get("humidity_percent"),
                pressure_hpa=weather_data.get("pressure_hpa"),
                wind_speed_ms=weather_data.get("wind_speed_ms"),
                clouds_percent=weather_data.get("clouds_percent"),
                uvi=weather_data.get("uvi"),
                weather_description=weather_data.get("weather_description")
            )

            session.add(record)
            session.commit()
            record_id = record.id
            session.close()

            logger.info(f"Données météo actuelles chargées (ID: {record_id})")
            return record_id

        except Exception as e:
            logger.error(f"Erreur lors du chargement des données météo: {e}")
            session.rollback()
            session.close()
            raise

    def load_forecasts(self, forecasts: List[Dict], latitude: float, longitude: float) -> int:
        """
        Charge les prévisions météo

        Args:
            forecasts: Liste des prévisions transformées
            latitude: Latitude
            longitude: Longitude

        Returns:
            Nombre de prévisions chargées
        """
        try:
            session = self.Session()

            forecast_records = []
            for forecast in forecasts:
                record = WeatherForecast(
                    forecast_date=forecast.get("date"),
                    latitude=latitude,
                    longitude=longitude,
                    temp_min=forecast.get("temp_min"),
                    temp_max=forecast.get("temp_max"),
                    temp_day=forecast.get("temp_day"),
                    humidity=forecast.get("humidity"),
                    pressure=forecast.get("pressure"),
                    wind_speed=forecast.get("wind_speed"),
                    rain_mm=forecast.get("rain_mm"),
                    pop=forecast.get("pop"),
                    uvi=forecast.get("uvi"),
                    temp_amplitude=forecast.get("temp_amplitude"),
                    water_stress_index=forecast.get("water_stress_index"),
                    et0_mm=forecast.get("et0_mm"),
                    irrigation_need_mm=forecast.get("irrigation_need_mm"),
                    disease_risk=forecast.get("disease_risk")
                )
                forecast_records.append(record)

            session.add_all(forecast_records)
            session.commit()
            count = len(forecast_records)
            session.close()

            logger.info(f"{count} prévisions chargées")
            return count

        except Exception as e:
            logger.error(f"Erreur lors du chargement des prévisions: {e}")
            session.rollback()
            session.close()
            raise

    def create_field(self, name: str, latitude: float, longitude: float,
                     crop_type: str = None, area_hectares: float = None,
                     metadata: Dict = None) -> int:
        """
        Crée un nouveau champ agricole

        Args:
            name: Nom du champ
            latitude: Latitude
            longitude: Longitude
            crop_type: Type de culture
            area_hectares: Surface en hectares
            metadata: Métadonnées additionnelles

        Returns:
            ID du champ créé
        """
        try:
            session = self.Session()

            field = AgriculturalField(
                name=name,
                latitude=latitude,
                longitude=longitude,
                crop_type=crop_type,
                area_hectares=area_hectares,
                metadata=metadata or {}
            )

            session.add(field)
            session.commit()
            field_id = field.id
            session.close()

            logger.info(f"Champ agricole créé (ID: {field_id})")
            return field_id

        except Exception as e:
            logger.error(f"Erreur lors de la création du champ: {e}")
            session.rollback()
            session.close()
            raise


def load_data_pipeline(transformed_data: Dict) -> Dict:
    """
    Pipeline complet de chargement des données

    Args:
        transformed_data: Données transformées

    Returns:
        Dict avec résultats du chargement
    """
    loader = DatabaseLoader()

    location = transformed_data.get("metadata", {}).get("location", {})
    latitude = location.get("latitude")
    longitude = location.get("longitude")

    # Chargement données actuelles
    weather_id = loader.load_current_weather(
        transformed_data.get("current_weather", {}),
        latitude,
        longitude
    )

    # Chargement prévisions
    forecast_count = loader.load_forecasts(
        transformed_data.get("forecasts", []),
        latitude,
        longitude
    )

    results = {
        "weather_record_id": weather_id,
        "forecast_count": forecast_count,
        "loaded_at": datetime.now().isoformat()
    }

    logger.info("Pipeline de chargement complété")
    return results


if __name__ == "__main__":
    # Test création d'un champ
    loader = DatabaseLoader()

    field_id = loader.create_field(
        name="Champ Test Dakar",
        latitude=14.7167,
        longitude=-17.4677,
        crop_type="riz",
        area_hectares=2.5
    )

    print(f"Champ créé avec ID: {field_id}")
