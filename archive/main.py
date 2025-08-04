from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import logging
import os

from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/predictions.log",         # Logs go to this file
    level=logging.INFO,                      # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()
model = joblib.load("models/best_model.pkl")
request_counter = Counter("predict_requests_total", "Total number of prediction requests")

class InputData(BaseModel):
    feature_vector: list[float]

@app.post("/predict")
def predict(data: InputData):
    request_counter.inc()
    X = np.array([data.feature_vector])
    prediction = model.predict(X)
    logging.info(f"Input: {data.feature_vector}, Prediction: {prediction.tolist()}")
    for handler in logging.getLogger().handlers:
        handler.flush()

    return {"prediction": prediction.tolist()}


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type="text/plain")