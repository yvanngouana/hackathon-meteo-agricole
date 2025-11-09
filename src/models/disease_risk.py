"""
Modèle de risque de maladies agricoles
Utilise des règles métier combinées à un modèle de classification
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
from typing import List, Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import xgboost as xgb
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

class DiseaseRiskModel:
    """
    Modèle de prédiction de risques de maladies agricoles
    """
    
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les features pour le modèle de risque de maladies
        
        Args:
            df: DataFrame avec données météo et agricoles historiques
            
        Returns:
            DataFrame avec features préparées
        """
        df = df.copy()
        
        # Convertir la date si nécessaire
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Calculer des indicateurs de risque
        # Humidité élevée favorise les maladies fongiques
        if 'humidity' in df.columns:
            df['high_humidity'] = (df['humidity'] > 75).astype(int)
            df['humidity_stress'] = np.where(df['humidity'] > 85, 2, np.where(df['humidity'] > 70, 1, 0))
        
        # Température dans la plage favorable aux maladies (15-30°C)
        if 'temp_day' in df.columns or 'temp_mean' in df.columns:
            temp_col = 'temp_day' if 'temp_day' in df.columns else 'temp_mean'
            df['optimal_disease_temp'] = np.where(
                (df[temp_col] >= 15) & (df[temp_col] <= 30), 1, 0
            )
            df['moderate_disease_temp'] = np.where(
                (df[temp_col] > 10) & (df[temp_col] < 35), 1, 0
            )
        
        # Température et humidité combinées (indicateur de stress)
        if 'humidity' in df.columns and ('temp_day' in df.columns or 'temp_mean' in df.columns):
            temp_col = 'temp_day' if 'temp_day' in df.columns else 'temp_mean'
            df['temp_humidity_index'] = df[temp_col] * df['humidity'] / 100
        
        # Précipitations récentes favorisent la propagation
        if 'rain_mm' in df.columns:
            for period in [1, 3, 7]:
                df[f'rain_cum_{period}d'] = df['rain_mm'].rolling(window=period, min_periods=1).sum()
        
        # Calculer un indicateur combiné de risque
        risk_factors = []
        if 'humidity_stress' in df.columns:
            risk_factors.append(df['humidity_stress'])
        if 'optimal_disease_temp' in df.columns:
            risk_factors.append(df['optimal_disease_temp'])
        if 'rain_cum_3d' in df.columns:
            risk_factors.append((df['rain_cum_3d'] > 5).astype(int) * 2)  # Poids plus important pour les pluies récentes
        
        if risk_factors:
            df['combined_risk_factor'] = sum(risk_factors)
        
        # Type de culture (si disponible) - encodage
        if 'crop_type' in df.columns:
            if not hasattr(self, '_crop_fitted'):
                df['crop_encoded'] = self.label_encoder.fit_transform(df['crop_type'].astype(str))
                self._crop_fitted = True
            else:
                # Gérer les nouvelles catégories non vues pendant l'entraînement
                df['crop_type_safe'] = df['crop_type'].astype(str)
                df['crop_type_safe'] = df['crop_type_safe'].apply(
                    lambda x: x if x in self.label_encoder.classes_ else 'unknown'
                )
                
                # Ré-entraîner l'encodeur si nécessaire
                unique_classes = set(list(self.label_encoder.classes_) + list(df['crop_type_safe'].unique()))
                temp_encoder = LabelEncoder()
                temp_encoder.fit(list(unique_classes))
                
                # Créer un mapping pour les anciennes classes
                temp_classes = temp_encoder.classes_
                old_class_indices = {cls: i for i, cls in enumerate(self.label_encoder.classes_)}
                
                # Créer un tableau temporaire pour les nouvelles affectations
                new_encoded = []
                for crop in df['crop_type_safe']:
                    if crop in old_class_indices:
                        new_encoded.append(old_class_indices[crop])
                    else:
                        # Assigner la même valeur que 'unknown' s'il existe, sinon 0
                        new_encoded.append(len(self.label_encoder.classes_) - 1 if 'unknown' in self.label_encoder.classes_ else 0)
                df['crop_encoded'] = new_encoded
        
        # Création de la cible (risque de maladie)
        # Définir le risque comme une combinaison de facteurs
        if 'combined_risk_factor' in df.columns:
            df['disease_risk_level'] = np.where(
                df['combined_risk_factor'] >= 4, 'high',
                np.where(df['combined_risk_factor'] >= 2, 'medium', 'low')
            )
        else:
            # Si pas d'indicateur combiné, créer à partir de conditions simples
            if 'humidity' in df.columns and 'temp_day' in df.columns:
                df['disease_risk_level'] = np.where(
                    (df['humidity'] > 80) & (df['temp_day'] > 15) & (df['temp_day'] < 30),
                    'high',
                    np.where(
                        (df['humidity'] > 70) & (df['temp_day'] > 10) & (df['temp_day'] < 35),
                        'medium',
                        'low'
                    )
                )
            else:
                df['disease_risk_level'] = 'low'  # Valeur par défaut
        
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
        if 'temp_day' not in df.columns:
            if 'temp_mean' in df.columns:
                df['temp_day'] = df['temp_mean']
            else:
                df['temp_day'] = 25.0
        
        if 'temp_mean' not in df.columns:
            df['temp_mean'] = df.get('temp_day', 25.0)
            
        if 'humidity' not in df.columns:
            df['humidity'] = 60.0
            
        if 'rain_mm' not in df.columns:
            df['rain_mm'] = 0.0
        
        if 'date' not in df.columns:
            df['date'] = [datetime.now() + timedelta(days=i) for i in range(len(df))]
        
        if 'crop_type' not in df.columns:
            df['crop_type'] = 'mixed'  # Valeur par défaut
        
        df = self._prepare_features(df)
        
        return df
    
    def train(self, historical_data: List[Dict]) -> Dict:
        """
        Entraîne le modèle de risque de maladies agricoles
        
        Args:
            historical_data: Données historiques avec indicateurs météo et agricoles
            
        Returns:
            Dictionnaire avec métriques d'évaluation
        """
        logger.info("Début de l'entraînement du modèle de risque de maladies")
        
        # Convertir les données en DataFrame
        df = pd.DataFrame(historical_data)
        
        # Remplir les colonnes manquantes avec des valeurs par défaut
        if 'date' not in df.columns:
            df['date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
        
        if 'temp_day' not in df.columns:
            if 'temp_mean' in df.columns:
                df['temp_day'] = df['temp_mean']
            else:
                df['temp_day'] = 25.0
        
        if 'temp_mean' not in df.columns:
            df['temp_mean'] = df.get('temp_day', 25.0)
            
        if 'humidity' not in df.columns:
            df['humidity'] = 60.0
            
        if 'rain_mm' not in df.columns:
            df['rain_mm'] = 0.0
            
        if 'crop_type' not in df.columns:
            df['crop_type'] = 'mixed'  # Valeur par défaut
        
        # Préparer les features
        df = self._prepare_features(df)
        
        # Colonnes de features (toutes les colonnes sauf la cible, la date et d'autres colonnes non numériques)
        feature_cols = [col for col in df.columns if col not in ['disease_risk_level', 'date', 'created_at', 'disease_risk']]
        
        # Vérifier qu'il y a suffisamment de données
        if len(df) < 10:
            raise ValueError("Données insuffisantes pour l'entraînement")
        
        # Encoder la cible
        if 'disease_risk_level' in df.columns:
            y_encoded = self.label_encoder.fit_transform(df['disease_risk_level'])
        else:
            # Si la colonne cible n'existe pas, la créer basée sur des règles métier
            temp_df = self._prepare_features(df)
            y_encoded = self.label_encoder.fit_transform(temp_df['disease_risk_level'])
        
        X = df[feature_cols]
        
        # Remplacer les valeurs infinies et les valeurs manquantes
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.mean())  # Remplacer les NaN par la moyenne
        
        # Diviser les données
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        
        # Entraîner le modèle Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
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
        class_report = classification_report(y_test, y_test_pred, 
                                           target_names=self.label_encoder.classes_,
                                           output_dict=True)
        
        # Calculer la matrice de confusion
        try:
            from sklearn.metrics import confusion_matrix
            conf_matrix = confusion_matrix(y_test, y_test_pred)
        except:
            conf_matrix = [[0]]  # Valeur par défaut si erreur
        
        # Calculer les features importantes
        feature_importance = dict(zip(feature_cols, self.model.feature_importances_))
        
        self.is_trained = True
        
        metrics = {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'classification_report': class_report,
            'confusion_matrix': conf_matrix.tolist() if hasattr(conf_matrix, 'tolist') else [[0]],
            'feature_importance': feature_importance
        }
        
        logger.info(f"Modèle entraîné - Test accuracy: {test_accuracy:.4f}")
        
        return metrics
    
    def predict(self, future_weather_data: List[Dict]) -> List[Dict]:
        """
        Prédit les risques de maladies agricoles
        
        Args:
            future_weather_data: Données météo futures
            
        Returns:
            Liste de dictionnaires avec prédictions de risque de maladies
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")
        
        # Préparer les features
        df = self._create_features_for_prediction(future_weather_data)
        
        # Colonnes de features
        feature_cols = [col for col in df.columns if col not in ['disease_risk_level', 'date', 'created_at', 'disease_risk']]
        
        # Vérifier que toutes les colonnes de features sont présentes, créer avec 0 si absentes
        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0.0
        
        # Remplacer les valeurs infinies et les valeurs manquantes
        df[feature_cols] = df[feature_cols].replace([np.inf, -np.inf], np.nan)
        df[feature_cols] = df[feature_cols].fillna(df[feature_cols].mean())
        
        X = df[feature_cols]
        
        # Faire les prédictions
        predictions_encoded = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        # Décoder les prédictions
        predictions = self.label_encoder.inverse_transform(predictions_encoded)
        
        # Créer les résultats
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            # La probabilité est la confiance dans la prédiction
            max_prob = np.max(prob)
            
            result = {
                'date': df.iloc[i]['date'].isoformat() if isinstance(df.iloc[i]['date'], pd.Timestamp) 
                        else str(df.iloc[i]['date']),
                'disease_risk_level': str(pred),
                'risk_probability': float(max_prob),
                'risk_factors': self._get_risk_factors(df.iloc[i])
            }
            results.append(result)
        
        return results
    
    def _get_risk_factors(self, row) -> Dict:
        """
        Obtient les facteurs de risque pour une ligne
        
        Args:
            row: Ligne de DataFrame
            
        Returns:
            Dictionnaire avec les facteurs de risque
        """
        factors = {}
        
        if 'high_humidity' in row.index and row['high_humidity'] == 1:
            factors['high_humidity'] = True
            
        if 'optimal_disease_temp' in row.index and row['optimal_disease_temp'] == 1:
            factors['optimal_temperature'] = True
            
        if 'temp_humidity_index' in row.index:
            factors['temp_humidity_index'] = float(row['temp_humidity_index'])
        
        return factors
    
    def save_model(self, filepath: str):
        """
        Sauvegarde le modèle entraîné
        
        Args:
            filepath: Chemin du fichier pour sauvegarder le modèle
        """
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
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
        self.label_encoder = model_data['label_encoder']
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
        temp_day = 25 + 10 * np.sin(2 * np.pi * i / 365.25) + np.random.normal(0, 3)
        humidity = max(30, min(95, 70 + 10 * np.sin(2 * np.pi * i / 365.25) + np.random.normal(0, 10)))
        rain_mm = max(0, np.random.exponential(0.5))
        
        # Simuler des conditions qui favorisent les maladies
        # Plus de risques pendant les périodes chaudes et humides
        if humidity > 80 and 15 < temp_day < 30:
            # Augmenter la probabilité de conditions favorables aux maladies
            humidity *= 1.2
            rain_mm += 1
        
        crop_type = np.random.choice(['rice', 'maize', 'millet', 'groundnut', 'cotton', 'mixed'])
        
        data.append({
            'date': date,
            'temp_day': temp_day,
            'temp_mean': temp_day,
            'humidity': humidity,
            'rain_mm': rain_mm,
            'crop_type': crop_type
        })
    
    return data


if __name__ == "__main__":
    # Exemple d'utilisation
    model = DiseaseRiskModel()
    
    # Créer des données d'exemple
    sample_data = create_sample_data()
    
    # Entraîner le modèle
    metrics = model.train(sample_data)
    print("Métriques d'entraînement:", metrics)
    
    # Faire une prédiction (en utilisant une partie des données comme exemple futur)
    future_data = sample_data[-14:]  # Derniers 14 jours comme exemple
    predictions = model.predict(future_data)
    
    print("\nPrédictions de risque de maladies:")
    for pred in predictions[:7]:  # Afficher les 7 premiers jours
        print(f"{pred['date']}: Niveau={pred['disease_risk_level']}, Probabilité={pred['risk_probability']:.2f}, Facteurs={pred['risk_factors']}")
    
    # Sauvegarder le modèle
    model.save_model("disease_risk_model.pkl")