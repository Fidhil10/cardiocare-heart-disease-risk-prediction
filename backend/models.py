from sqlalchemy import Column, Integer, String, Float
from .database import Base

class PredictionHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True)
    Age = Column(Integer)
    Sex = Column(String)
    ChestPainType = Column(String)
    RestingBP = Column(Integer)
    Cholesterol = Column(Integer)
    FastingBS = Column(Integer)
    RestingECG = Column(String)
    MaxHR = Column(Integer)
    ExerciseAngina = Column(String)
    Oldpeak = Column(Float)
    ST_Slope = Column(String)
    PredictionResult = Column(Integer) # 1 for heart disease, 0 for normal
