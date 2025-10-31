from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from . import database
from .schemas import PatientCreate

app = FastAPI()

#create data base
models.Base.metadata.create_all(bind=database.engine)

#load ML  model
ML_MODEL = None
MODEL_PATH = 'models/model_rf.joblib'

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
     return {"patient_id" : id_patient}

@app.post("/patients", response_model=PatientCreate)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    new_patient= models.Patient(**data.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


