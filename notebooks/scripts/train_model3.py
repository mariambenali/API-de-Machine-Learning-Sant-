import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score


# --- FONCTIONS UTILES ---

def load_data(file_path) :
    """
    Charge le dataset CSV, et effectue l'encodage de la variable cible 'status' (positive/negative -> 1/0).
    """
    print("-> Chargement et Encodage initial des données...")
    df = pd.read_csv(file_path)
    
    #  ENCODAGE DE LA VARIABLE CIBLE 
    df['status'] = df['status'].map({'positive': 1, 'negative': 0})

    return df

def preprocess_data(df) :
    """
    Prépare les données pour le modèle ML.
    """
    print("-> Préparation des données ")
    
    # X (Features) : toutes les colonnes sauf 'status'
    X = df.drop('status', axis=1)
    # y (Target) : la colonne 'status' (qui est maintenant numérique 0/1)
    y = df['status']
    
    return X, y

def create_and_train_pipeline(X_train, y_train) :
    """Définit le pipeline de ML avec RandomForest et l'entraîne."""
    print("-> Définition et Entraînement du Pipeline (RandomForest)...")

    pipeline = Pipeline([
        # Standardisation 
        ('scaler', StandardScaler()),
        # Classifieur
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Entraînement
    pipeline.fit(X_train, y_train)
    
    print("   - Entraînement terminé.")
    return pipeline

def evaluate_model(pipeline, X_test, y_test):
    """Évalue le modèle entraîné en affichant les métriques clés."""
    print("-> Évaluation du modèle sur l'ensemble de test...")
    y_pred = pipeline.predict(X_test)
    
    
    accuracy = accuracy_score(y_test, y_pred)
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    
    # Les paramètres pos_label=1 fonctionnent car la cible est 0/1
    f1_positive = f1_score(y_test, y_pred, pos_label=1)
    precision_positive = precision_score(y_test, y_pred, pos_label=1)
    recall_positive = recall_score(y_test, y_pred, pos_label=1)
    
    # Affichage des résultats
    print("\n--- Métriques de Performance ---")
    print(f"Exactitude (Accuracy) Totale: {accuracy:.4f}")
    print(f"F1-Score (Pondéré): {f1_weighted:.4f}")
    print(f"--- Focus sur la classe POSITIVE (Risque Cardiaque) ---")
    print(f"Précision (Positive): {precision_positive:.4f}")
    print(f"Rappel (Recall) (Positive): {recall_positive:.4f}")
    print(f"F1-Score (Positive): {f1_positive:.4f}")
    
    # Rapport complet (ajustement des noms pour coller à 0/1)
    print("\n--- Rapport de Classification Complet ---")
    print(classification_report(y_test, y_pred, target_names=['Négatif (0)', 'Positif (1)']))

def save_model(pipeline, file_path):
    """Sauvegarde le pipeline entraîné."""
    print(f"-> Sauvegarde du modèle dans : {file_path}")
    joblib.dump(pipeline, file_path)
    print("   - Modèle sauvegardé avec succès.")

# --- LOGIQUE PRINCIPALE ---

if __name__ == "__main__":
    DATA_PATH = 'data/data.csv'
    MODEL_PATH = 'models/model_rf.joblib' 
    
    # Chargement et Pré-traitement (maintenant correct)
    df = load_data(DATA_PATH)
    X, y = preprocess_data(df)

    # Séparation des données
    # Pourquoi stratify=y ? Pour s'assurer que la proportion de 'positive' et 'negative'
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Entraînement, Évaluation et Sauvegarde
    pipeline = create_and_train_pipeline(X_train, y_train)
    evaluate_model(pipeline, X_test, y_test)
    save_model(pipeline, MODEL_PATH)
    
    
# Verification du fonctionnement de modele   
    
myModel=joblib.load(MODEL_PATH)
patient_data = {
    'age': 64,
    'gender': 1,
    'pressurehight': 160,
    'pressurelow': 83,
    'glucose': 160,
    'kcm': 1.80,
    'troponin': 0.012,
    'impluse': 66
}
   
new_df =pd.DataFrame([patient_data])
newPrediction=myModel.predict(new_df)

print(f"my new prediction :{newPrediction}")