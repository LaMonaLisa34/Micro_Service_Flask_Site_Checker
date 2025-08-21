# Site Checker – Microservice Flask

Ce microservice permet de **vérifier automatiquement si un site web est en ligne**, en envoyant une requête HTTP.  
Il est conçu pour être intégré à une **architecture microservices** (Prometheus, Grafana, etc.).

---

## 📦 Dépendances

Le fichier `requirements.txt` contient les dépendances suivantes :

- `flask`  
- `requests`  
- `python-dotenv`  
- `prometheus_client`  
- `pytest`  

---

## ⚙️ Fonctionnement

Le microservice lit une variable `SITE_TO_CHECK` depuis un fichier `.env`, puis expose deux routes principales :

| Méthode | Route         | Description                                     |
|--------:|---------------|-------------------------------------------------|
| `GET`   | `/check-site` | Envoie une requête HTTP vers le site ciblé     |
| `GET`   | `/metrics`    | Expose les métriques au format Prometheus      |

**Exemple de réponse :**
```json
{
  "url": "https://exemple.com",
  "status": "success",
  "code": 200,
  "message": "Site https://exemple.com is reachable."
}
```

---

## 🧪 Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/LaMonaLisa34/Micro_Service_Flask_Site_Checker.git
cd Micro_Service_Flask_Site_Checker

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sous Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer un fichier .env
echo "SITE_TO_CHECK=https://exemple.com" > .env

# 5. Lancer l’application
python run.py
```

---

## 🐳 Utilisation avec Docker

```bash
# Construire l'image
docker build -t site_checker .

# Lancer le conteneur avec le port mappé et la variable d’environnement
docker run -d -p 5050:5000 --env-file .env --name site_checker site_checker
```

---

## 📈 Monitoring Prometheus

Le service expose des métriques Prometheus à l’URL `/metrics`.

### Métriques disponibles :

| Nom                          | Type    | Description                               |
|-----------------------------|---------|-------------------------------------------|
| `checker_requests_total`    | Counter | Nombre total de vérifications             |
| `checker_status_codes_total`| Counter | Nombre de codes HTTP par type             |
| `checker_last_status`       | Gauge   | Dernier code HTTP observé                 |

### Exemple de configuration Prometheus :

```yaml
scrape_configs:
  - job_name: 'site_checker_flask'
    static_configs:
      - targets: ['<IP_VM>:5050']
```

---

## 📊 Dashboard Grafana

Un dashboard prêt à l’importation est fourni dans ce dépôt :  
➡️ `grafana_dashboard_site_checker.json`

### Instructions d’import :

1. Aller dans **Grafana > Dashboards > Import**
2. Copier-coller le contenu du fichier JSON ou le téléverser
3. Choisir **Prometheus** comme datasource
4. Si nécessaire, adapter l'UID dans le JSON (`__YOUR_PROMETHEUS_UID__`) ou le laisser vide

---