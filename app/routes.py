from flask import Blueprint, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/check-site', methods=["GET", "POST"])
def check_site():
    site_url = os.getenv("SITE_TO_CHECK")

    if not site_url:
        return jsonify({
            'status': 'error',
            'message': 'No URL provided in .env file.'
        }), 400

    try:
        res = requests.get(site_url, timeout=5)
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
        return jsonify({
            'url': site_url,
            'status': 'error',
            'message': f'Request failed: {str(e)}'
        }), 500
