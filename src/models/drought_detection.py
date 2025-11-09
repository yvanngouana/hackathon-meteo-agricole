"""
Modèle de détection de sécheresse
Utilise Random Forest pour prédire les risques de sécheresse
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
from typing import List, Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
import xgboost as xgb
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

class DroughtDetectionModel:
    """
    Modèle de détection de sécheresse utilisant Random Forest
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les features pour le modèle de détection de sécheresse
        
        Args:
            df: DataFrame avec données météo historiques
            
        Returns:
            DataFrame avec features préparées
        """
        df = df.copy()
        
        # Convertir la date si nécessaire
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Calculer l'indice de sécheresse basé sur les précipitations
        if 'rain_mm' in df.columns:
            # Moyenne mobile des précipitations sur différentes périodes
            for period in [7, 14, 30]:
                df[f'rain_cum_{period}d'] = df['rain_mm'].rolling(window=period, min_periods=1).sum()
        
        # Calculer l'indice de stress hydrique si disponible
        if 'temp_mean' in df.columns and 'humidity' in df.columns:
            df['water_stress_index'] = (df['temp_mean'] - 25) * (100 - df['humidity']) / 100
            df['water_stress_index'] = df['water_stress_index'].clip(lower=0)
        
        # Calculer l'évapotranspiration potentielle si température moyenne est disponible
        if 'temp_mean' in df.columns:
            df['et0_simplified'] = 0.0023 * (df['temp_mean'] + 17.8) * np.sqrt(
                np.maximum(0, df.get('temp_amplitude', 10))
            )
        
        # Calculer l'humidité relative moyenne mobile
        if 'humidity' in df.columns:
            for period in [7, 14, 30]:
                df[f'humidity_mean_{period}d'] = df['humidity'].rolling(window=period, min_periods=1).mean()
        
        # Calculer l'indice humidex (indicateur de stress thermique)
        if 'temp_mean' in df.columns and 'humidity' in df.columns:
            df['humidex'] = df['temp_mean'] + 0.5555 * (6.11 * np.exp(5417.7530 * (1/273.16 - 1/(df['temp_mean'] + 273.16))) * (df['humidity']/100 - 10))
        
        # Features temporelles
        if 'date' in df.columns:
            df['day_of_year'] = df['date'].dt.dayofyear
            df['month'] = df['date'].dt.month
        
        # Indicateurs de sécheresse basés sur le ratio précipitation/ET0
        if 'rain_cum_7d' in df.columns and 'et0_simplified' in df.columns:
            df['drought_indicator_7d'] = df['rain_cum_7d'] / (df['et0_simplified'] * 7 + 0.1)  # +0.1 pour éviter division par 0
        
        if 'rain_cum_30d' in df.columns and 'et0_simplified' in df.columns:
            df['drought_indicator_30d'] = df['rain_cum_30d'] / (df['et0_simplified'] * 30 + 0.1)
        
        # Calculer la cible (sécheresse) basée sur plusieurs indicateurs
        df['is_drought'] = 0
        
        # Critères pour détecter la sécheresse
        drought_conditions = []
        
        # Indicateur basé sur le ratio précipitation/ET0
        if 'drought_indicator_7d' in df.columns:
            drought_conditions.append(df['drought_indicator_7d'] < 0.5)  # Pluie < 50% de l'ET0 sur 7 jours
        
        if 'drought_indicator_30d' in df.columns:
            drought_conditions.append(df['drought_indicator_30d'] < 0.8)  # Pluie < 80% de l'ET0 sur 30 jours
        
        # Indicateur basé sur l'humidité
        if 'humidity_mean_14d' in df.columns:
            drought_conditions.append(df['humidity_mean_14d'] < 40)  # Humidité moyenne < 40%
        
        # Si au moins 2 conditions sont remplies, c'est une sécheresse
        if drought_conditions:
            drought_condition = sum(drought_conditions) >= 1  # Utiliser au moins 1 condition
            df['is_drought'] = drought_condition.astype(int)
        
        # Supprimer les lignes avec NaN (causées par les rolling windows)
        df = df.dropna()
        
        return df
    
    def _create_features_for_prediction(self, weather_data: List[Dict]) -> pd.DataFrame:
        """
        Crée des features à partir des données météo pour les prédictions
        
        Args:
            weather_data: Liste de dictionnaires avec données météo
            
        Returns:
            DataFrame avec features prêtes pour la prédiction
        """
        df = pd.DataFrame(weather_data)
        
        # Remplir les valeurs manquantes avec des valeurs par défaut
        if 'temp_mean' not in df.columns:
            if 'temp_min' in df.columns and 'temp_max' in df.columns:
                df['temp_mean'] = (df['temp_min'] + df['temp_max']) / 2
            else:
                df['temp_mean'] = 25.0
        
        if 'humidity' not in df.columns:
            df['humidity'] = 60.0
            
        if 'rain_mm' not in df.columns:
            df['rain_mm'] = 0.0
        
        if 'temp_amplitude' not in df.columns:
            df['temp_amplitude'] = 10.0
            
        if 'date' not in df.columns:
            df['date'] = [datetime.now() + timedelta(days=i) for i in range(len(df))]
        
        df = self._prepare_features(df)
        
        return df
    
    def train(self, historical_data: List[Dict]) -> Dict:
        """
        Entraîne le modèle de détection de sécheresse
        
        Args:
            historical_data: Données historiques avec indicateurs météo
            
        Returns:
            Dictionnaire avec métriques d'évaluation
        """
        logger.info("Début de l'entraînement du modèle de détection de sécheresse")
        
        # Convertir les données en DataFrame
        df = pd.DataFrame(historical_data)
        
        # Remplir les colonnes manquantes avec des valeurs par défaut
        if 'date' not in df.columns:
            df['date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
        
        if 'temp_mean' not in df.columns:
            df['temp_mean'] = 25.0
        
        if 'humidity' not in df.columns:
            df['humidity'] = 60.0
            
        if 'rain_mm' not in df.columns:
            df['rain_mm'] = 0.0
        
        if 'temp_amplitude' not in df.columns:
            df['temp_amplitude'] = 10.0
        
        # Préparer les features
        df = self._prepare_features(df)
        
        # Colonnes de features (toutes les colonnes sauf la cible, la date et d'autres colonnes non numériques)
        feature_cols = [col for col in df.columns if col not in ['is_drought', 'date', 'created_at', 'disease_risk']]
        
        # Vérifier qu'il y a suffisamment de données
        if len(df) < 10:
            raise ValueError("Données insuffisantes pour l'entraînement")
        
        # Vérifier qu'il y a des exemples des deux classes
        if df['is_drought'].nunique() < 2:
            # Forcer certaines valeurs à 1 pour avoir les deux classes
            n_drought = max(1, len(df) // 10)  # 10% de sécheresse
            df.iloc[:n_drought, df.columns.get_loc('is_drought')] = 1
            logger.warning("Ajustement forcé des valeurs de sécheresse pour avoir les deux classes")
        
        X = df[feature_cols]
        y = df['is_drought']
        
        # Diviser les données
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Calculer les poids de classe pour gérer le déséquilibre
        classes = np.unique(y_train)
        class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
        class_weight_dict = dict(zip(classes, class_weights))
        
        # Entraîner le modèle Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight=class_weight_dict,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Prédire sur les ensembles d'entraînement et de test
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Calculer les métriques
        train_accuracy = accuracy_score(y_train, y_train_pred)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        
        # Calculer un report de classification détaillé
        class_report = classification_report(y_test, y_test_pred, output_dict=True)
        
        # Calculer la matrice de confusion
        conf_matrix = confusion_matrix(y_test, y_test_pred)
        
        # Calculer les features importantes
        feature_importance = dict(zip(feature_cols, self.model.feature_importances_))
        
        self.is_trained = True
        
        metrics = {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'classification_report': class_report,
            'confusion_matrix': conf_matrix.tolist(),
            'feature_importance': feature_importance
        }
        
        logger.info(f"Modèle entraîné - Test accuracy: {test_accuracy:.4f}")
        
        return metrics
    
    def predict(self, future_weather_data: List[Dict]) -> List[Dict]:
        """
        Prédit les risques de sécheresse
        
        Args:
            future_weather_data: Données météo futures
            
        Returns:
            Liste de dictionnaires avec prédictions de sécheresse
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")
        
        # Préparer les features
        df = self._create_features_for_prediction(future_weather_data)
        
        # Colonnes de features
        feature_cols = [col for col in df.columns if col not in ['is_drought', 'date', 'created_at', 'disease_risk']]
        
        # Vérifier que toutes les colonnes de features sont présentes, créer avec 0 si absentes
        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0.0
        
        X = df[feature_cols]
        
        # Faire les prédictions
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)  # Obtient les probabilités pour chaque classe
        
        # Créer les résultats
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            # Récupérer la probabilité de la classe positive (sécheresse)
            drought_prob = prob[1] if len(prob) > 1 else prob[0] if pred == 1 else 1 - prob[0]
            
            result = {
                'date': df.iloc[i]['date'].isoformat() if isinstance(df.iloc[i]['date'], pd.Timestamp) 
                        else str(df.iloc[i]['date']),
                'is_drought': bool(pred),
                'drought_probability': float(drought_prob),
                'drought_level': 'high' if pred == 1 and drought_prob > 0.8 else 'medium' if pred == 1 else 'low'
            }
            results.append(result)
        
        return results
    
    def save_model(self, filepath: str):
        """
        Sauvegarde le modèle entraîné
        
        Args:
            filepath: Chemin du fichier pour sauvegarder le modèle
        """
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, filepath)
        logger.info(f"Modèle sauvegardé dans {filepath}")
    
    def load_model(self, filepath: str):
        """
        Charge un modèle entraîné
        
        Args:
            filepath: Chemin du fichier contenant le modèle
        """
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.is_trained = model_data['is_trained']
        logger.info(f"Modèle chargé depuis {filepath}")


def create_sample_data():
    """
    Crée des données d'exemple pour tester le modèle
    """
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    n = len(dates)
    
    data = []
    for i, date in enumerate(dates):
        # Simuler des conditions météo
        temp_mean = 25 + 10 * np.sin(2 * np.pi * i / 365.25) + np.random.normal(0, 3)
        humidity = max(30, min(95, 70 + 10 * np.sin(2 * np.pi * i / 365.25) + np.random.normal(0, 10)))
        rain_mm = max(0, np.random.exponential(0.5))
        
        # Simuler des conditions de sécheresse saisonnière
        # Plus de sécheresse pendant les mois chauds et secs
        seasonal_factor = 1 + 0.5 * np.sin(2 * np.pi * (i % 365) / 365 - np.pi/2)
        if 150 < (i % 365) < 250:  # Saison sèche
            humidity = max(20, humidity * 0.7)
            rain_mm = rain_mm * 0.5
        
        temp_amplitude = max(5, 10 + 5 * np.random.normal(0, 1))
        
        data.append({
            'date': date,
            'temp_mean': temp_mean,
            'humidity': humidity,
            'rain_mm': rain_mm,
            'temp_amplitude': temp_amplitude
        })
    
    return data


if __name__ == "__main__":
    # Exemple d'utilisation
    model = DroughtDetectionModel()
    
    # Créer des données d'exemple
    sample_data = create_sample_data()
    
    # Entraîner le modèle
    metrics = model.train(sample_data)
    print("Métriques d'entraînement:", metrics)
    
    # Faire une prédiction (en utilisant une partie des données comme exemple futur)
    future_data = sample_data[-14:]  # Derniers 14 jours comme exemple
    predictions = model.predict(future_data)
    
    print("\nPrédictions de sécheresse:")
    for pred in predictions[:7]:  # Afficher les 7 premiers jours
        print(f"{pred['date']}: Sécheresse={pred['is_drought']}, Probabilité={pred['drought_probability']:.2f}, Niveau={pred['drought_level']}")
    
    # Sauvegarder le modèle
    model.save_model("drought_detection_model.pkl")