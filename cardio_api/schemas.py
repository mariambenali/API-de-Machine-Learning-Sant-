from pydantic import BaseModel


class PatientCreate(BaseModel):
    age: int
    gender : str
    pressure_hight :int
    pressure_low : int
    glucose : float
    kcm: float
    troponin: float
    impluse: int

class Patient(PatientCreate):
    id : int

