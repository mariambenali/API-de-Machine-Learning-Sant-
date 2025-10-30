from sqlalchemy import Column, Integer, Float
from cardio_api.databases import Base



class Patient(Base):
    __tablename__ = "patients"

    id= Column(Integer, primary_key=True ,index=True)
    age= Column(Integer)
    gender = Column(Integer)
    pressure_hight = Column(Integer)
    pressure_low= Column(Integer)
    glucose = Column(Float)
    kcm= Column(Float)
    troponin= Column(Float)
    impluse= Column(Integer)
    
    

