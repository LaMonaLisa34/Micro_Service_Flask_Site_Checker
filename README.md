# Site Checker – Microservice Flask

Ce microservice permet de **vérifier si un site web est atteignable** via une requête HTTP.  
Il est développé avec **Flask** et prévu pour s’intégrer dans une architecture en microservices (Kafka, Prometheus, etc.).

---   

## Dependances
flask
pytest
requests
python-dotenv

## Fonctionnement

Le service expose une route POST :
Il retourne un JSON contenant le statut d’accessibilité du site configuré dans un fichier `.env`.

---

## Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/LaMonaLisa34/Micro_Service_Flask_Site_Checker.git
cd nom-du-repo

# 2. Créer et activer un environnement virtuel
python -m venv .venv  
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l’application
python run.py