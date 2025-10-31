from sqlalchemy import Column, Integer, Float
from . database import Base



class Patient(Base):
    __tablename__ = "patients"

    id= Column(Integer, primary_key=True ,index=True)
    age= Column(Integer)
    gender = Column(Integer)
    pressurehight = Column(Integer)
    pressurelow= Column(Integer)
    glucose = Column(Float)
    kcm= Column(Float)
    troponin= Column(Float)
    impluse= Column(Integer)
    
    

