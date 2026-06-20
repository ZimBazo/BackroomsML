from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
import joblib

app = FastAPI()

model = joblib.load('../../models/best_model_v1.pkl')

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
    age: int
    sex: str
    height_cm: int
    weight_kg: int
    strength: int
    reaction: int
    stamina: int
    speed: int
    intelligence: int
    perception: int
    agility: int
    endurance: int
    stress_resistance: int
    luck: int
    panic: int
    fatigue: int
    hunger: int
    thirst: int
    mental_stability: int
    focus: int
    confidence: int
    pain_tolerance: int
    # has_flashlight: int
    flashlight_battery: int
    has_knife: int
    # has_backpack: int
    # has_first_aid_kit: int
    medkit_count: int
    # has_water: int
    water_amount: int
    # has_food: int
    food_amount: int
    has_radio: int
    level_id: str
    level_difficulty: int
    visibility: int
    entity_density: int
    entity_aggression: int
    resource_density: int
    maze_complexity: int
    geometry_stability: int
    special_rule: str
    spawn_area_danger: int
    distance_to_nearest_entity: int
    noise_generated: int
    time_since_last_encounter: int

@app.post('/predict')
def prediction_func(data: PredictionRequest):
    # Mapping for categorical fields
    sex_male = 1 if data.sex == 'male' else 0
    sex_other = 1 if data.sex == 'other' else 0
    
    level_ids = ['1', '2', '3', '4', '5', '6', '7', '8', 'end']
    level_id_dummies = [1 if data.level_id == lid else 0 for lid in level_ids]
    
    special_rules = ['darkness', 'flooding', 'haunted_hotel', 'liminal_office', 'mechanical_noise', 'neutral', 'resource_rich', 'trap_exit']
    special_rule_dummies = [1 if data.special_rule == sr else 0 for sr in special_rules]
    
    features = [
        data.age, data.height_cm, data.weight_kg, data.strength, data.reaction,
        data.stamina, data.speed, data.intelligence, data.perception, data.agility,
        data.endurance, data.stress_resistance, data.luck, data.panic, data.fatigue,
        data.hunger, data.thirst, data.mental_stability, data.focus, data.confidence,
        data.pain_tolerance, data.flashlight_battery, data.has_knife, data.medkit_count,
        data.water_amount, data.food_amount, data.has_radio,
        data.level_difficulty, data.visibility, data.entity_density, data.entity_aggression,
        data.resource_density, data.maze_complexity, data.geometry_stability,
        data.spawn_area_danger, data.distance_to_nearest_entity, data.noise_generated,
        data.time_since_last_encounter,
        sex_male, sex_other,
        *level_id_dummies,
        *special_rule_dummies
    ]
    
    logger.warning(f'Data features: {features}')

    proba = float(model.predict_proba([features])[0][1])
    pred = 1 if proba >= 0.65 else 0

    logger.warning(f'Prediction: {pred}, Probability: {proba}')

    return {
        'prediction': int(pred),
        'probability': float(proba)
    }