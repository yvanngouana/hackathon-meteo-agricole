"""
Module de transformation et nettoyage des données
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta
from loguru import logger


class WeatherDataTransformer:
    """Transforme les données météo brutes en format exploitable"""

    @staticmethod
    def transform_current_weather(raw_data: Dict) -> Dict:
        """
        Transforme les données météo actuelles

        Args:
            raw_data: Données brutes de l'API OpenWeather

        Returns:
            Dict avec données transformées et nettoyées
        """
        try:
            current = raw_data.get("current", {})

            transformed = {
                "timestamp": datetime.fromtimestamp(current.get("dt", 0)),
                "temperature_celsius": current.get("temp"),
                "feels_like_celsius": current.get("feels_like"),
                "humidity_percent": current.get("humidity"),
                "pressure_hpa": current.get("pressure"),
                "wind_speed_ms": current.get("wind_speed"),
                "clouds_percent": current.get("clouds"),
                "uvi": current.get("uvi"),
                "weather_description": current.get("weather", [{}])[0].get("description", "")
            }

            # Gestion des valeurs manquantes
            for key, value in transformed.items():
                if value is None:
                    logger.warning(f"Valeur manquante pour {key}")
                    transformed[key] = np.nan if key != "weather_description" else "unknown"

            logger.info("Données météo actuelles transformées")
            return transformed

        except Exception as e:
            logger.error(f"Erreur transformation données météo: {e}")
            raise

    @staticmethod
    def transform_forecast(raw_forecasts: List[Dict]) -> pd.DataFrame:
        """
        Transforme les prévisions météo en DataFrame

        Args:
            raw_forecasts: Liste des prévisions brutes

        Returns:
            DataFrame avec prévisions transformées
        """
        try:
            forecasts = []

            for forecast in raw_forecasts:
                transformed = {
                    "date": datetime.fromtimestamp(forecast.get("dt", 0)),
                    "temp_min": forecast.get("temp", {}).get("min"),
                    "temp_max": forecast.get("temp", {}).get("max"),
                    "temp_day": forecast.get("temp", {}).get("day"),
                    "humidity": forecast.get("humidity"),
                    "pressure": forecast.get("pressure"),
                    "wind_speed": forecast.get("wind_speed"),
                    "clouds": forecast.get("clouds"),
                    "rain_mm": forecast.get("rain", 0),  # Précipitations
                    "pop": forecast.get("pop", 0) * 100,  # Probabilité de pluie en %
                    "uvi": forecast.get("uvi")
                }
                forecasts.append(transformed)

            df = pd.DataFrame(forecasts)

            # Nettoyage des valeurs aberrantes
            df = df.replace([np.inf, -np.inf], np.nan)

            logger.info(f"{len(df)} prévisions transformées")
            return df

        except Exception as e:
            logger.error(f"Erreur transformation prévisions: {e}")
            raise

    @staticmethod
    def calculate_derived_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule des indicateurs dérivés pour le ML

        Args:
            df: DataFrame avec données météo

        Returns:
            DataFrame enrichi avec features dérivées
        """
        try:
            # Température moyenne journalière
            if "temp_min" in df.columns and "temp_max" in df.columns:
                df["temp_mean"] = (df["temp_min"] + df["temp_max"]) / 2

            # Amplitude thermique (indicateur de stress pour les plantes)
            if "temp_max" in df.columns and "temp_min" in df.columns:
                df["temp_amplitude"] = df["temp_max"] - df["temp_min"]

            # Indice de stress hydrique (température élevée + faible humidité)
            if "temp_max" in df.columns and "humidity" in df.columns:
                df["water_stress_index"] = (df["temp_max"] - 25) * (100 - df["humidity"]) / 100
                df["water_stress_index"] = df["water_stress_index"].clip(lower=0)

            # Évapotranspiration potentielle (formule simplifiée Hargreaves)
            if "temp_mean" in df.columns and "temp_amplitude" in df.columns:
                df["et0_mm"] = 0.0023 * (df["temp_mean"] + 17.8) * df["temp_amplitude"] ** 0.5

            # Besoin en irrigation (ET0 - pluie)
            if "et0_mm" in df.columns and "rain_mm" in df.columns:
                df["irrigation_need_mm"] = (df["et0_mm"] - df["rain_mm"]).clip(lower=0)

            # Risque maladie (humidité élevée + température modérée)
            if "humidity" in df.columns and "temp_day" in df.columns:
                df["disease_risk"] = np.where(
                    (df["humidity"] > 70) & (df["temp_day"] > 15) & (df["temp_day"] < 30),
                    "high",
                    np.where(
                        (df["humidity"] > 60) & (df["temp_day"] > 10) & (df["temp_day"] < 35),
                        "medium",
                        "low"
                    )
                )

            logger.info(f"{len(df.columns)} features après enrichissement")
            return df

        except Exception as e:
            logger.error(f"Erreur calcul features dérivées: {e}")
            raise


def transform_data_pipeline(raw_data: Dict) -> Dict:
    """
    Pipeline complet de transformation des données

    Args:
        raw_data: Données brutes extraites

    Returns:
        Dict avec données transformées
    """
    transformer = WeatherDataTransformer()

    # Transformation données actuelles
    current_weather = transformer.transform_current_weather(raw_data.get("weather", {}))

    # Transformation prévisions
    forecasts_df = transformer.transform_forecast(raw_data.get("forecast", []))

    # Calcul features dérivées
    forecasts_enriched = transformer.calculate_derived_features(forecasts_df)

    transformed_data = {
        "current_weather": current_weather,
        "forecasts": forecasts_enriched.to_dict(orient="records"),
        "metadata": {
            "transformed_at": datetime.now().isoformat(),
            "location": raw_data.get("location", {}),
            "num_forecasts": len(forecasts_enriched)
        }
    }

    logger.info("Pipeline de transformation complété")
    return transformed_data


if __name__ == "__main__":
    # Test avec données exemple
    from extract import extract_all_data

    DAKAR_LAT = 14.7167
    DAKAR_LON = -17.4677

    raw_data = extract_all_data(DAKAR_LAT, DAKAR_LON)
    transformed = transform_data_pipeline(raw_data)

    print(f"Données transformées: {list(transformed.keys())}")
    print(f"Nombre de prévisions: {len(transformed['forecasts'])}")
