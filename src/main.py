from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("models/best_model.pkl")

class InputData(BaseModel):
    feature_vector: list[float]

@app.post("/predict")
def predict(data: InputData):
    X = np.array([data.feature_vector])
    prediction = model.predict(X)
    return {"prediction": prediction.tolist()}
