import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)


PATIENT = {
    "age": 40,
    "gender": 0,
    "pressurehight": 120,
    "pressurelow": 75,
    "glucose": 80.0,
    "kcm": 1.0,
    "troponin": 0.005,
    "impluse": 70
    }

def test_predict_risk():
    response = client.post("/predict_risk", json=PATIENT)
    assert response.status_code == 200

