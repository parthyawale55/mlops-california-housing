from fastapi import FastAPI, HTTPException
from api.schemas import HouseFeatures
import joblib
import numpy as np
import logging
import os
import subprocess

from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse

# Set up logging directory and format
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/predictions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Prometheus counter
request_counter = Counter("predict_requests_total", "Total number of prediction requests")

# Load FastAPI app and model
app = FastAPI()
model_path = "models/best_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError("Model not found at expected path.")
model = joblib.load(model_path)

@app.post("/predict")
def predict(features: HouseFeatures):
    request_counter.inc()

    input_data = np.array([[v for v in features.dict().values()]])
    prediction = model.predict(input_data)[0]

    logging.info(f"Input: {features.dict()}, Prediction: {prediction}")
    for handler in logging.getLogger().handlers:
        handler.flush()

    return {"prediction": prediction}

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type="text/plain")

@app.post("/retrain")
def retrain_model():
    try:
        result = subprocess.run(["python", "src/retrain.py"], capture_output=True, text=True)
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout.strip()}
        else:
            raise RuntimeError(result.stderr.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
