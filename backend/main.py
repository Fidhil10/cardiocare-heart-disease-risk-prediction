import joblib
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Heart Disease Prediction API")

# Load model
try:
    model = joblib.load('heart_pred.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict", response_model=schemas.PredictResponse)
def predict_heart_disease(request: schemas.PredictRequest, db: Session = Depends(get_db)):
    if model is None:
        raise HTTPException(status_code=500, detail="ML model not loaded properly.")
    
    # Map features to the one-hot encoded dataframe format the model expects
    # Model feature order:
    # ['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak', 'Sex_M',
    #  'ChestPainType_ATA', 'ChestPainType_NAP', 'ChestPainType_TA',
    #  'RestingECG_Normal', 'RestingECG_ST', 'ExerciseAngina_Y', 'ST_Slope_Flat',
    #  'ST_Slope_Up']
    
    data = {
        'Age': [request.Age],
        'RestingBP': [request.RestingBP],
        'Cholesterol': [request.Cholesterol],
        'FastingBS': [request.FastingBS],
        'MaxHR': [request.MaxHR],
        'Oldpeak': [request.Oldpeak],
        'Sex_M': [1 if request.Sex == 'M' else 0],
        'ChestPainType_ATA': [1 if request.ChestPainType == 'ATA' else 0],
        'ChestPainType_NAP': [1 if request.ChestPainType == 'NAP' else 0],
        'ChestPainType_TA': [1 if request.ChestPainType == 'TA' else 0],
        'RestingECG_Normal': [1 if request.RestingECG == 'Normal' else 0],
        'RestingECG_ST': [1 if request.RestingECG == 'ST' else 0],
        'ExerciseAngina_Y': [1 if request.ExerciseAngina == 'Y' else 0],
        'ST_Slope_Flat': [1 if request.ST_Slope == 'Flat' else 0],
        'ST_Slope_Up': [1 if request.ST_Slope == 'Up' else 0],
    }

    df = pd.DataFrame(data)
    
    # Prediction
    prediction = int(model.predict(df)[0])

    # Save to history
    history_record = models.PredictionHistory(
        patient_name=request.patient_name,
        Age=request.Age,
        Sex=request.Sex,
        ChestPainType=request.ChestPainType,
        RestingBP=request.RestingBP,
        Cholesterol=request.Cholesterol,
        FastingBS=request.FastingBS,
        RestingECG=request.RestingECG,
        MaxHR=request.MaxHR,
        ExerciseAngina=request.ExerciseAngina,
        Oldpeak=request.Oldpeak,
        ST_Slope=request.ST_Slope,
        PredictionResult=prediction
    )
    db.add(history_record)
    db.commit()
    db.refresh(history_record)

    return {"prediction": prediction}

@app.get("/history", response_model=List[schemas.HistoryResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(models.PredictionHistory).all()
