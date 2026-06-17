from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger

app = FastAPI()

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

class TextClaim(BaseModel):
    name: str
    surname: str

@app.post('/text-claim')
def text_claim(data: TextClaim):
    text = data.model_dump()
    logger.info(f'Backend. data: {text}')
    
    return text