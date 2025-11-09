"""
DAG Airflow pour l'ETL automatisé des données météo
Exécution quotidienne pour collecter et stocker les données
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sys
sys.path.append('/opt/airflow/src')

from etl.extract import extract_all_data
from etl.transform import transform_data_pipeline
from etl.load import load_data_pipeline


# Configuration par défaut du DAG
default_args = {
    'owner': 'hack2hire-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Définition du DAG
dag = DAG(
    'weather_etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL pour données météo et agricoles',
    schedule_interval='0 6 * * *',  # Tous les jours à 6h00
    start_date=days_ago(1),
    catchup=False,
    tags=['meteo', 'agricole', 'etl'],
)


def extract_weather_data(**context):
    """Task: Extraction des données météo"""
    # Exemple: Plusieurs localités au Sénégal
    locations = [
        {"name": "Dakar", "lat": 14.7167, "lon": -17.4677},
        {"name": "Saint-Louis", "lat": 16.0179, "lon": -16.5119},
        {"name": "Thiès", "lat": 14.7886, "lon": -16.9260},
    ]

    all_data = []
    for location in locations:
        data = extract_all_data(location["lat"], location["lon"])
        data["location_name"] = location["name"]
        all_data.append(data)

    # Stocker dans XCom pour la tâche suivante
    context['ti'].xcom_push(key='raw_data', value=all_data)

    return f"Extraction réussie pour {len(all_data)} localités"


def transform_weather_data(**context):
    """Task: Transformation des données"""
    # Récupérer les données de la tâche précédente
    raw_data_list = context['ti'].xcom_pull(key='raw_data', task_ids='extract_data')

    transformed_data_list = []
    for raw_data in raw_data_list:
        transformed = transform_data_pipeline(raw_data)
        transformed["location_name"] = raw_data.get("location_name")
        transformed_data_list.append(transformed)

    # Stocker dans XCom
    context['ti'].xcom_push(key='transformed_data', value=transformed_data_list)

    return f"Transformation réussie pour {len(transformed_data_list)} localités"


def load_weather_data(**context):
    """Task: Chargement dans PostgreSQL"""
    # Récupérer les données transformées
    transformed_data_list = context['ti'].xcom_pull(key='transformed_data', task_ids='transform_data')

    results = []
    for transformed_data in transformed_data_list:
        result = load_data_pipeline(transformed_data)
        result["location_name"] = transformed_data.get("location_name")
        results.append(result)

    return f"Chargement réussi pour {len(results)} localités"


# Définition des tâches
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_weather_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_weather_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_weather_data,
    provide_context=True,
    dag=dag,
)

# Définition des dépendances
extract_task >> transform_task >> load_task
