# Utiliser l'image officielle Python comme image parente.
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR C:/Users/mathy/OneDrive - Ynov/Mathys/ynov/3éme Année/Projet Spé/Archi docker

# Copier les fichiers de dépendances dans le conteneur.
COPY python/hello.py .
COPY python/requirements.txt .

# Installer les dépendances.
RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python", "./hello.py"]