from fastapi import FastAPI
from api.schemas import HouseFeatures
import joblib
import numpy as np

app = FastAPI()

# Load the best model
model = joblib.load("models/best_model.pkl")  # ← You’ll create this in next step

@app.post("/predict")
def predict(features: HouseFeatures):
    input_data = np.array([[v for v in features.dict().values()]])
    prediction = model.predict(input_data)[0]
    return {"prediction": prediction}
