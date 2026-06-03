from pydantic import BaseModel

class PredictRequest(BaseModel):
    patient_name: str
    Age: int
    Sex: str
    ChestPainType: str
    RestingBP: int
    Cholesterol: int
    FastingBS: int
    RestingECG: str
    MaxHR: int
    ExerciseAngina: str
    Oldpeak: float
    ST_Slope: str

class PredictResponse(BaseModel):
    prediction: int

class HistoryResponse(PredictRequest):
    id: int
    PredictionResult: int

    class Config:
        from_attributes = True
