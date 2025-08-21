from flask import Blueprint, jsonify
import os
import requests
from dotenv import load_dotenv
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

from dotenv import load_dotenv

main = Blueprint('main', __name__)

# --- Metrics Prometheus ---
http_requests_total = Counter("checker_requests_total", "Nombre total de checks")
http_status_codes = Counter("checker_status_codes", "Codes HTTP renvoyés", ["code"])
last_status = Gauge("checker_last_status", "Dernier code HTTP observé")

@main.route('/check-site', methods=["GET", "POST"])
def check_site():
    site_url = os.getenv("SITE_TO_CHECK")

    if not site_url:
        return jsonify({
            'status': 'error',
            'message': 'No URL provided in .env file.'
        }), 400

    http_requests_total.inc()  # chaque appel compte

    try:
        res = requests.get(site_url, timeout=5)
        http_status_codes.labels(code=str(res.status_code)).inc()
        last_status.set(res.status_code)

        if res.status_code == 200:
            return jsonify({
                'url': site_url,
                'status': 'success',
                'code': res.status_code,
                'message': f'Site {site_url} is reachable.'
            })
        else:
            return jsonify({
                'url': site_url,
                'status': 'warning',
                'code': res.status_code,
                'message': f'Site responded with status code {res.status_code}.'
            })
    except requests.exceptions.RequestException as e:
        http_status_codes.labels(code="error").inc()
        last_status.set(-1)
        return jsonify({
            'url': site_url,
            'status': 'error',
            'message': f'Request failed: {str(e)}'
        }), 500

# --- Endpoint Prometheus ---
@main.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)