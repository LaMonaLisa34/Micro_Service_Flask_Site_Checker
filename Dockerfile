# Utilise une image officielle Python comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définir la variable d’environnement pour désactiver le buffering Python
ENV PYTHONUNBUFFERED=1

# Spécifie le port sur lequel l'app écoute
EXPOSE 5000

# Démarrer l'application Flask
CMD ["python", "run.py"]
