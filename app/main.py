from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models
from . import database
from .schemas import PatientCreate
import joblib  
import pandas as pd 

app = FastAPI()

#  Chargement du modèle ML au démarrage de l'application
ML_MODEL = None
MODEL_PATH = 'models/model_rf.joblib'

try:
    ML_MODEL = joblib.load(MODEL_PATH)
    print(f"Modèle ML chargé avec succès depuis {MODEL_PATH}")
except FileNotFoundError:
    ML_MODEL = None
    print(f"ERREUR CRITIQUE: Modèle ML non trouvé à {MODEL_PATH}. Veuillez exécuter train_model.py.")

#create data base
models.Base.metadata.create_all(bind=database.engine)



#create session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
     return db.query(models.Patient).all()

@app.get("/patients/{id_patient}",response_model=PatientCreate)
def get_patients(id_patient:int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == id_patient).first()
    return patient

@app.post("/patients", response_model=PatientCreate)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    new_patient= models.Patient(**data.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient




#  ENDPOINT DE PRÉDICTION

@app.post("/predict_risk")
def predict_risk(data: PatientCreate):
   
    if ML_MODEL is None:
        raise HTTPException(status_code=503, detail="Service indisponible : Modèle ML non chargé.")

    # Conversion des données Pydantic en DataFrame Pandas
    patient_data_dict = data.model_dump() 
    patient_df = pd.DataFrame([patient_data_dict]) 
    #  Prédiction via le Pipeline
    prediction = ML_MODEL.predict(patient_df)
    
    # Prédiction de probabilité 
    probability = ML_MODEL.predict_proba(patient_df)[0][1]

    #  Formatage de la réponse
    result_code = int(prediction[0])
    prediction_status = "positive" if result_code == 1 else "negative"

    return {
        "prediction_code": result_code,
        "prediction_status": prediction_status,
        "message": f"Le modèle prédit un risque cardiaque : {prediction_status}",
        "message": f"Probabilité pour la classe 1 : {probability}"
        
    }


