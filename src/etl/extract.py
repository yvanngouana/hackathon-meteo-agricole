"""
Module d'extraction des données depuis les APIs externes
- OpenWeather One Call 3.0
- FAO/FAOSTAT
- Copernicus
"""

import os
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import random
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class WeatherDataExtractor:
    """Extracteur de données météorologiques depuis OpenWeather API"""

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = os.getenv("OPENWEATHER_BASE_URL", "https://api.openweathermap.org/data/3.0")
        self.use_mock = os.getenv("USE_MOCK_DATA", "False").lower() == "true"

        if not self.api_key and not self.use_mock:
            raise ValueError("OPENWEATHER_API_KEY n'est pas définie dans .env")

    def _generate_mock_weather_data(self, latitude: float, longitude: float) -> Dict:
        """
        Génère des données météo simulées réalistes pour le développement

        Args:
            latitude: Latitude
            longitude: Longitude

        Returns:
            Dict avec structure identique à OpenWeather API
        """
        now = datetime.now()

        # Données actuelles simulées (climat tropical africain)
        current = {
            "dt": int(now.timestamp()),
            "temp": random.uniform(25, 35),  # Températures typiques Afrique
            "feels_like": random.uniform(26, 37),
            "humidity": random.randint(40, 85),
            "pressure": random.randint(1010, 1020),
            "wind_speed": random.uniform(2, 8),
            "clouds": random.randint(10, 90),
            "uvi": random.uniform(6, 12),
            "weather": [{"description": random.choice([
                "clear sky", "few clouds", "scattered clouds",
                "light rain", "moderate rain", "partly cloudy"
            ])}]
        }

        # Prévisions 7 jours simulées
        daily = []
        for day in range(7):
            forecast_date = now + timedelta(days=day)
            temp_base = random.uniform(24, 34)

            daily_forecast = {
                "dt": int(forecast_date.timestamp()),
                "temp": {
                    "min": temp_base - random.uniform(3, 6),
                    "max": temp_base + random.uniform(2, 5),
                    "day": temp_base
                },
                "humidity": random.randint(45, 80),
                "pressure": random.randint(1010, 1020),
                "wind_speed": random.uniform(2, 10),
                "clouds": random.randint(10, 90),
                "rain": random.uniform(0, 15) if random.random() > 0.4 else 0,
                "pop": random.uniform(0.1, 0.9),
                "uvi": random.uniform(6, 11)
            }
            daily.append(daily_forecast)

        mock_data = {
            "lat": latitude,
            "lon": longitude,
            "current": current,
            "daily": daily
        }

        logger.info(f"Données MOCK générées pour ({latitude}, {longitude})")
        return mock_data

    def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """
        Récupère les données météo actuelles pour une localisation

        Args:
            latitude: Latitude du champ agricole
            longitude: Longitude du champ agricole

        Returns:
            Dict contenant les données météo actuelles
        """
        # Mode MOCK pour développement sans API
        if self.use_mock:
            return self._generate_mock_weather_data(latitude, longitude)

        try:
            url = f"{self.base_url}/onecall"
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
                "units": "metric",  # Celsius
                "exclude": "minutely,alerts"
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Données météo récupérées pour ({latitude}, {longitude})")

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la récupération des données météo: {e}")
            raise

    def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> List[Dict]:
        """
        Récupère les prévisions météo pour les prochains jours

        Args:
            latitude: Latitude du champ agricole
            longitude: Longitude du champ agricole
            days: Nombre de jours de prévision

        Returns:
            Liste des prévisions journalières
        """
        try:
            data = self.get_current_weather(latitude, longitude)
            forecasts = data.get("daily", [])[:days]

            logger.info(f"Prévisions {days} jours récupérées pour ({latitude}, {longitude})")

            return forecasts

        except Exception as e:
            logger.error(f"Erreur lors de la récupération des prévisions: {e}")
            raise


class AgriculturalDataExtractor:
    """Extracteur de données agricoles depuis FAO et Copernicus"""

    def __init__(self):
        self.fao_api_key = os.getenv("FAO_API_KEY")
        self.fao_base_url = os.getenv("FAO_BASE_URL", "https://fenixservices.fao.org/faostat/api/v1")

    def get_crop_data(self, country_code: str = "SN", crop: str = "rice") -> pd.DataFrame:
        """
        Récupère les données de production agricole depuis FAO

        Args:
            country_code: Code pays (ex: SN pour Sénégal)
            crop: Type de culture

        Returns:
            DataFrame avec les données agricoles
        """
        try:
            # TODO: Implémenter l'appel API FAO
            # Pour l'instant, retourne des données exemple
            logger.warning("Utilisation de données agricoles simulées")

            data = {
                "crop": [crop] * 5,
                "year": [2019, 2020, 2021, 2022, 2023],
                "production_tons": [100000, 105000, 98000, 110000, 112000],
                "area_hectares": [50000, 51000, 49000, 52000, 53000]
            }

            return pd.DataFrame(data)

        except Exception as e:
            logger.error(f"Erreur lors de la récupération des données FAO: {e}")
            raise


def extract_all_data(latitude: float, longitude: float) -> Dict:
    """
    Fonction principale pour extraire toutes les données nécessaires

    Args:
        latitude: Latitude du champ
        longitude: Longitude du champ

    Returns:
        Dict contenant toutes les données extraites
    """
    weather_extractor = WeatherDataExtractor()
    agri_extractor = AgriculturalDataExtractor()

    data = {
        "timestamp": datetime.now().isoformat(),
        "location": {"latitude": latitude, "longitude": longitude},
        "weather": weather_extractor.get_current_weather(latitude, longitude),
        "forecast": weather_extractor.get_forecast(latitude, longitude),
        "agricultural_data": agri_extractor.get_crop_data().to_dict()
    }

    logger.info("Extraction complète des données réussie")

    return data


if __name__ == "__main__":
    # Exemple: Dakar, Sénégal
    DAKAR_LAT = 14.7167
    DAKAR_LON = -17.4677

    data = extract_all_data(DAKAR_LAT, DAKAR_LON)
    print(f"Données extraites: {list(data.keys())}")
