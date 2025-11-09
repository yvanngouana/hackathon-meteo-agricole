"""
Modèle de prédiction de pluie
Utilise Random Forest pour prédire la quantité de pluie
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
from loguru import logger
from typing import Dict, Optional
import os


class RainPredictor:
    """
    Modèle de prédiction de pluie basé sur Random Forest
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialise le prédicteur de pluie

        Args:
            model_path: Chemin vers le modèle sauvegardé (optionnel)
        """
        self.model = None
        self.is_trained = False
        self.feature_names = [
            'temp_day', 'temp_min', 'temp_max', 'humidity',
            'pressure', 'wind_speed', 'clouds', 'pop'
        ]

        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            # Créer un modèle pré-entraîné par défaut
            self._create_pretrained_model()

    def _create_pretrained_model(self):
        """Crée et entraîne un modèle par défaut avec données synthétiques"""
        logger.info("Création d'un modèle pré-entraîné par défaut...")

        # Générer données synthétiques
        np.random.seed(42)
        n_samples = 500

        data = {
            'temp_day': np.random.uniform(20, 35, n_samples),
            'temp_min': np.random.uniform(15, 25, n_samples),
            'temp_max': np.random.uniform(25, 40, n_samples),
            'humidity': np.random.uniform(30, 95, n_samples),
            'pressure': np.random.uniform(1000, 1025, n_samples),
            'wind_speed': np.random.uniform(0, 15, n_samples),
            'clouds': np.random.uniform(0, 100, n_samples),
            'pop': np.random.uniform(0, 100, n_samples),
        }

        df = pd.DataFrame(data)

        # Target: pluie basée sur humidité, nébulosité et probabilité
        df['rain_mm'] = (
            (df['humidity'] / 100) * 10 +
            (df['clouds'] / 100) * 8 +
            (df['pop'] / 100) * 12 +
            np.random.normal(0, 2, n_samples)
        )
        df['rain_mm'] = df['rain_mm'].clip(lower=0)

        X = df[self.feature_names]
        y = df['rain_mm']

        self.model = RandomForestRegressor(
            n_estimators=50,
            max_depth=8,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X, y)
        self.is_trained = True

        logger.info("Modèle pré-entraîné créé avec succès")

    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les features pour le modèle

        Args:
            df: DataFrame avec données météo

        Returns:
            DataFrame avec features préparées
        """
        # Sélectionner les features pertinentes
        features = df[self.feature_names].copy()

        # Gérer les valeurs manquantes
        features = features.fillna(features.mean())

        return features

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Prédit la quantité de pluie

        Args:
            X: Features pour prédiction

        Returns:
            Array avec prédictions (mm de pluie)
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")

        predictions = self.model.predict(X)

        # S'assurer que les prédictions sont positives
        predictions = np.maximum(predictions, 0)

        return predictions

    def predict_single(self, weather_features: Dict) -> float:
        """
        Prédit la pluie pour un seul jour

        Args:
            weather_features: Dict avec les features météo

        Returns:
            Prédiction de pluie en mm
        """
        # Créer DataFrame avec features
        df = pd.DataFrame([weather_features])
        X = self.prepare_features(df)

        prediction = self.predict(X)[0]

        return float(prediction)

    def save_model(self, path: str):
        """Sauvegarde le modèle"""
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant d'être sauvegardé")

        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)
        logger.info(f"Modèle sauvegardé: {path}")

    def load_model(self, path: str):
        """Charge un modèle sauvegardé"""
        self.model = joblib.load(path)
        self.is_trained = True
        logger.info(f"Modèle chargé: {path}")


if __name__ == "__main__":
    # Test du modèle
    predictor = RainPredictor()

    # Test prédiction
    test_weather = {
        'temp_day': 28,
        'temp_min': 22,
        'temp_max': 33,
        'humidity': 75,
        'pressure': 1013,
        'wind_speed': 5,
        'clouds': 60,
        'pop': 70
    }

    prediction = predictor.predict_single(test_weather)
    print(f"Prédiction de pluie: {prediction:.1f}mm")
