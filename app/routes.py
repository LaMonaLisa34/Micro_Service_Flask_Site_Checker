# Importation des modules nécessaires
from flask import Blueprint, jsonify, Response
import os
import requests
from http import HTTPStatus
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Création d'un Blueprint Flask pour modulariser l'application
main = Blueprint('main', __name__)

# --- Définition des métriques Prometheus ---

# Compteur global du nombre total de vérifications effectuées
http_requests_total = Counter("checker_requests_total", "Nombre total de checks")
# Compteur des codes de réponse HTTP reçus (ex : 200, 404, 500, etc.)
http_status_codes = Counter("checker_status_codes", "Codes HTTP renvoyés", ["code"])
# Jauge qui garde la trace du dernier code HTTP observé (ex : 200 ou -1 si erreur)
last_status = Gauge("checker_last_status", "Dernier code HTTP observé")

# --- Route principale pour tester un site ---
@main.route('/check-site', methods=["GET", "POST"])
def check_site():
    # Récupération de l’URL à tester depuis la variable d’environnement
    site_url = os.getenv("SITE_TO_CHECK")

    if not site_url:
        return jsonify({
            'status': 'error',
            'message': 'No URL provided in .env file.'
        }), 400

    http_requests_total.inc()

    try:
        res = requests.get(site_url, timeout=5)
        http_status_codes.labels(code=str(res.status_code)).inc()
        last_status.set(res.status_code)

        # Détermination de la catégorie du statut
        status_code = res.status_code
        if 200 <= status_code < 300:
            status_category = "success"
        elif 300 <= status_code < 400:
            status_category = "redirect"
        elif 400 <= status_code < 500:
            status_category = "client_error"
        elif 500 <= status_code < 600:
            status_category = "server_error"
        else:
            status_category = "unknown"

        # Libellé HTTP standard (ex: OK, Not Found, etc.)
        status_text = HTTPStatus(status_code).phrase if status_code in HTTPStatus.__members__.values() else ""

        return jsonify({
            'url': site_url,
            'status': status_category,
            'code': status_code,
            'label': status_text,
            'message': f'Site responded with status code {status_code}.'
        })

    except requests.exceptions.RequestException as e:
        http_status_codes.labels(code="error").inc()
        last_status.set(-1)
        return jsonify({
            'url': site_url,
            'status': 'error',
            'message': f'Request failed: {str(e)}'
        }), 500

# --- Route pour exposer les métriques à Prometheus ---
@main.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
