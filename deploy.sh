#!/bin/bash

# ==================== SCRIPT DE DÉPLOIEMENT AUTOMATISÉ ====================
# Plateforme Intelligence Météo & Agricole
# Usage: ./deploy.sh [dev|prod]

set -e  # Arrêter en cas d'erreur

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher des messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier les arguments
ENV=${1:-dev}

if [ "$ENV" != "dev" ] && [ "$ENV" != "prod" ]; then
    log_error "Usage: $0 [dev|prod]"
    exit 1
fi

log_info "Déploiement en mode: $ENV"

# ==================== VÉRIFICATIONS PRÉREQUIS ====================

log_info "Vérification des prérequis..."

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    log_error "Docker n'est pas installé. Installez-le d'abord."
    exit 1
fi

# Vérifier Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose n'est pas installé."
    exit 1
fi

log_info "✓ Docker et Docker Compose installés"

# ==================== CONFIGURATION ====================

if [ "$ENV" == "prod" ]; then
    COMPOSE_FILE="docker-compose.production.yml"
    ENV_FILE=".env.production"

    # Vérifier .env.production
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Fichier $ENV_FILE manquant. Copiez .env.production.example et configurez-le."
        exit 1
    fi

    # Vérifier variables critiques
    source $ENV_FILE
    if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" == "CHANGE_ME_SECRET_KEY_32_CHARS_MIN" ]; then
        log_error "SECRET_KEY non configurée dans $ENV_FILE"
        exit 1
    fi

    log_info "✓ Configuration production validée"
else
    COMPOSE_FILE="docker-compose.yml"
    ENV_FILE=".env"

    if [ ! -f "$ENV_FILE" ]; then
        log_warn "Fichier .env manquant. Copie de .env.example..."
        cp .env.example .env
    fi
fi

# ==================== ARRÊT DES SERVICES EXISTANTS ====================

log_info "Arrêt des services existants..."
docker-compose -f $COMPOSE_FILE down 2>/dev/null || true

# ==================== BUILD DES IMAGES ====================

log_info "Build des images Docker..."
docker-compose -f $COMPOSE_FILE build

# ==================== DÉMARRAGE DES SERVICES ====================

log_info "Démarrage des services..."
docker-compose -f $COMPOSE_FILE up -d

# ==================== ATTENTE SANTÉ DES SERVICES ====================

log_info "Attente du démarrage des services..."
sleep 10

# Vérifier PostgreSQL
log_info "Vérification PostgreSQL..."
for i in {1..30}; do
    if docker-compose -f $COMPOSE_FILE exec -T postgres pg_isready -U postgres &> /dev/null; then
        log_info "✓ PostgreSQL prêt"
        break
    fi
    if [ $i -eq 30 ]; then
        log_error "PostgreSQL ne démarre pas"
        exit 1
    fi
    sleep 2
done

# Vérifier API
log_info "Vérification API..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health &> /dev/null; then
        log_info "✓ API prête"
        break
    fi
    if [ $i -eq 30 ]; then
        log_error "API ne démarre pas"
        docker-compose -f $COMPOSE_FILE logs api
        exit 1
    fi
    sleep 2
done

# ==================== INITIALISATION BASE DE DONNÉES ====================

log_info "Initialisation de la base de données..."
docker-compose -f $COMPOSE_FILE exec -T api python -c "
from etl.load import DatabaseLoader
try:
    loader = DatabaseLoader()
    loader.create_tables()
    print('Tables créées avec succès!')
except Exception as e:
    print(f'Tables déjà créées ou erreur: {e}')
" || log_warn "Erreur création tables (peuvent déjà exister)"

# ==================== TESTS POST-DÉPLOIEMENT ====================

log_info "Tests post-déploiement..."

# Test Health Check
HEALTH=$(curl -s http://localhost:8000/health | grep -o "healthy")
if [ "$HEALTH" == "healthy" ]; then
    log_info "✓ Health check OK"
else
    log_error "Health check échoué"
    exit 1
fi

# Test API Weather
WEATHER=$(curl -s "http://localhost:8000/api/weather/current?latitude=14.7167&longitude=-17.4677" | grep -o "temperature_celsius")
if [ ! -z "$WEATHER" ]; then
    log_info "✓ API Weather OK"
else
    log_error "API Weather échouée"
fi

# ==================== AFFICHAGE STATUT ====================

echo ""
log_info "=========================================="
log_info "  DÉPLOIEMENT RÉUSSI - MODE $ENV"
log_info "=========================================="
echo ""

# Afficher les URLs
if [ "$ENV" == "prod" ]; then
    log_info "URLs de production:"
    log_info "  - Frontend:  https://votre-domaine.com"
    log_info "  - API Docs:  https://votre-domaine.com/docs"
    log_info "  - Airflow:   https://votre-domaine.com/airflow (interne)"
else
    log_info "URLs de développement:"
    log_info "  - Frontend:  http://localhost:3000"
    log_info "  - API:       http://localhost:8000"
    log_info "  - API Docs:  http://localhost:8000/docs"
    log_info "  - Airflow:   http://localhost:8080 (admin/admin)"
    log_info "  - MLflow:    http://localhost:5000"
fi

echo ""
log_info "Commandes utiles:"
log_info "  - Logs:      docker-compose -f $COMPOSE_FILE logs -f"
log_info "  - Status:    docker-compose -f $COMPOSE_FILE ps"
log_info "  - Arrêter:   docker-compose -f $COMPOSE_FILE down"
log_info "  - Redémarrer: docker-compose -f $COMPOSE_FILE restart"

echo ""
log_info "✅ Déploiement terminé avec succès!"
