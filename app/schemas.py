from pydantic import BaseModel


class PatientCreate(BaseModel):
    age: int
    gender : int
    pressurehight :int
    pressurelow : int
    glucose : float
    kcm: float
    troponin: float
    impluse: int

class Patient(PatientCreate):
    id : int

