import joblib
import os

def load_model():
    MODEL_DIR = os.path.join(os.getcwd(), 'models')
    print(MODEL_DIR)

load_model()