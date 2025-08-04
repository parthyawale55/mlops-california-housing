from fastapi.testclient import TestClient
from api.app import app  # Import your FastAPI app

client = TestClient(app)

def test_predict_endpoint():
    # Provide a realistic input example based on your model's schema
    sample_input = {
        "longitude": -122.23,
        "latitude": 37.88,
        "housing_median_age": 41.0,
        "total_rooms": 880.0,
        "total_bedrooms": 129.0,
        "population": 322.0,
        "households": 126.0,
        "median_income": 8.3252
    }

    response = client.post("/predict", json=sample_input)
    assert response.status_code == 200
    assert "prediction" in response.json()
