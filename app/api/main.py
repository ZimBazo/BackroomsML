from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
import joblib

app = FastAPI()

model = joblib.load('../../models/Streamlit_test_model.pkl')

origins = [
    'http://127.0.0.1:8501',
    'http://localhost:8501'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class PredictionRequest(BaseModel):
    fatigue: int
    panic: int
    thirst: int
    reaction: int
    hunger: int
    # # dataframe_for_pydantic = df_temp[['fatigue', 'panic', 'thirst', 'reaction', 'hunger', 'survived_24h']]

@app.post('/predict')
def prediction_func(data: PredictionRequest):
    data = [[data.fatigue, data.panic, data.thirst, data.reaction, data.hunger]]
    logger.warning(f'Data: {data}')
    pred = model.predict(data)
    logger.warning(f'Prediction: {pred}')
    return 'Good'