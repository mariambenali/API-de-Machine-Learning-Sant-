#  API de Prédiction du Risque Cardiaque (Cardio-API)

Ce projet implémente une API RESTful basée sur FastAPI et SQLAlchemy pour :

1. Enregistrer des données de patients dans une base de données SQLite.
2. Fournir un endpoint de Machine Learning (`/predict_risk`) pour évaluer le risque cardiaque d'un patient donné, en utilisant un modèle pré-entraîné (Random Forest) sérialisé avec `joblib`.

##  Prérequis

Pour exécuter ce projet, vous avez besoin de :

- Python (version 3.8+)
- Un environnement virtuel recommandé (`venv` ou `conda`)

## Installation et Lancement

Suivez ces étapes pour configurer et lancer l'API.

### 1. Cloner le Dépôt (si applicable)
```bash
git clone <URL_DE_VOTRE_DEPOT>
cd API-de-Machine-Learning-Sant-
```

### 2. Création et Activation de l'Environnement Virtuel
```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement (Linux/macOS)
source venv/bin/activate

# Activer l'environnement (Windows)
.\venv\Scripts\activate
```

### 3. Installation des Dépendances

Installez tous les paquets nécessaires :
```bash
pip install fastapi uvicorn sqlalchemy pydantic joblib pandas httpx pytest scikit-learn
```

### 4. Entraînement et Export du Modèle ML (Tâche IA)

**Crucial** : L'API nécessite la présence du fichier `models/model_rf.joblib`. Vous devez exécuter votre script d'entraînement pour générer ce fichier.
```bash
# Assurez-vous d'avoir un script qui génère models/model_rf.joblib
# Exemple :
python notebooks/scripts/train_model.py
```

### 5. Lancement de l'API

L'API est lancée en mode rechargement (reload) avec Uvicorn.
```bash
uvicorn app.main:app --reload
```

L'API sera disponible à l'adresse : `http://127.0.0.1:8000`

##  Utilisation de l'API (Endpoints)

La documentation interactive Swagger est disponible à : `http://127.0.0.1:8000/docs`

### 1. Endpoint de Machine Learning

| Méthode | Chemin | Description | Données Requises (JSON) | Réponse |
|---------|--------|-------------|------------------------|---------|
| `POST` | `/predict_risk` | Prédit le risque cardiaque d'un patient. | `PatientCreate` Schema | Code de prédiction (0 ou 1) et statut. |

**Exemple de Requête JSON pour la prédiction :**
```json
{
    "age": 65,
    "gender": 1,
    "pressurehight": 180,
    "pressurelow": 100,
    "glucose": 250.0,
    "kcm": 15.0,
    "troponin": 0.5,
    "impluse": 110
}
```

### 2. Endpoints CRUD (Base de Données)

| Méthode | Chemin | Description | Réponse |
|---------|--------|-------------|---------|
| `GET` | `/patients` | Récupère la liste de tous les patients enregistrés. | Liste des objets `Patient`. |
| `POST` | `/patients` | Enregistre un nouveau patient dans la DB. | L'objet `Patient` créé avec son `id`. |
| `GET` | `/patients/{id}` | Récupère un patient spécifique par ID. | Objet `Patient`. |

## Structure du Projet

| Fichier/Dossier | Description |
|-----------------|-------------|
| `app/` | Contient la logique principale de l'API. |
| ├── `main.py` | Le point d'entrée FastAPI, définit les endpoints et intègre le modèle ML. |
| ├── `databases.py` | Configuration de la connexion SQLAlchemy et de la DB SQLite. |
| ├── `models.py` | Modèles de données pour SQLAlchemy (table `patients`). |
| ├── `schemas.py` | Schémas de données Pydantic pour la validation des requêtes (`PatientCreate`) et des réponses (`Patient`). |
| `models/` | Contient le modèle de Machine Learning . |
| ├── `model_rf.joblib` | Le modèle Random Forest pré-entraîné (Pipeline). |
| `tests/` | Contient les tests unitaires pour l'API. |
| ├── `test_prediction.py` | Tests pour valider l'endpoint `/predict_risk` et le statut `200`. |
| `README.md` | Ce fichier. |

## Tests Unitaires

Le projet utilise Pytest pour garantir que les endpoints fonctionnent comme prévu, notamment l'intégration du modèle ML.

1. Assurez-vous d'être à la racine du projet.
2. Exécutez Pytest :
```bash
pytest
```

Les tests vérifient la disponibilité de l'API (status `200`) et la cohérence des prédictions du modèle pour des cas de faible et haut risque connus.

## Contact et Auteurs

- AYOUB MOTEI : Intégration ML, Tests, Documentation.
- MARIAM BENALI : Base de données (SQLAlchemy), Endpoints CRUD.