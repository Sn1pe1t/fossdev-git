import requests
import numpy as np
from fastapi import FastAPI

app = FastAPI()

@app.get("/mean")
def compute_mean() -> dict:
    data = np.array([10, 20, 30, 40, 50])
    return {"mean": float(np.mean(data))}

def get_external_data() -> dict:
    resp = requests.get('https://httpbin.org/get')
    return resp.json()

# Необязательный вызов для проверки (не влияет на импорт в FastAPI)
if __name__ == '__main__':
    print(get_external_data())