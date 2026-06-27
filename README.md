# BackroomsML

  The project is a complete machine learning cycle for predicting the survival of characters in a simulated environment (Backrooms). The system covers all the main stages of work: creation of synthetic data, training and evaluation of the model, as well as its deployment using the API and web interface.
  


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571.svg?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2A8A3E.svg?style=for-the-badge)

![GitHub stars](https://img.shields.io/github/stars/ZimBazo/BackroomsML?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/ZimBazo/BackroomsML?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/ZimBazo/BackroomsML?style=for-the-badge)
![License](https://img.shields.io/github/license/ZimBazo/BackroomsML?style=for-the-badge)



<img width="1576" height="1080" alt="Tets" src="https://github.com/user-attachments/assets/3fc9ab77-bff3-42ab-8655-90f9923dfb35" />

## Why This Project
BackroomsML is a project where I have identified a full-scale toolkit for staff training in the Backroomsml world. It includes all the settings, from creating a GUI to uploading the API and web interface to docker.

Most of these projects use ready-made datasets, but I wanted to follow this path from the very beginning. I decided to create my own dataset based on my favorite kripipasta, and with such a structure that the model could not just remember the patterns. The main difficulty was to make the data quite complex. In the first versions, the usual logistic regression immediately showed high results, and complex tree models did not provide any advantage against its background. Because of this, I had to redo the generation algorithm several times.

In the final version, about fifty different characteristics affect survival. There are many non-linear relationships and hidden factors that change depending on the user's chosen level. In such conditions, gradient boosting works significantly better than simple linear models, because it is able to capture these complex dependencies.
## Dataset Schema

50 columns (4 groups):

| Group | Columns |
|-------|---------|
| Demographics & stats | age, sex, height_cm, weight_kg, strength, reaction, stamina, speed, intelligence, perception, agility, endurance, stress_resistance, luck |
| Psychological state | panic, fatigue, hunger, thirst, mental_stability, focus, confidence, pain_tolerance |
| Inventory | has_flashlight, flashlight_battery, has_knife, has_backpack, has_first_aid_kit, medkit_count, has_water, water_amount, has_food, food_amount, has_radio |
| Environment & targets | level_id, level_difficulty, visibility, entity_density, entity_aggression, resource_density, maze_complexity, geometry_stability, special_rule, spawn_area_danger, distance_to_nearest_entity, noise_generated, time_since_last_encounter, survived_24h, survival_time_hours, escape_probability |

## Model Training

Three targets can be trained independently:
- **survived_24h** (binary classification) — the primary model
- **survival_time_hours** (regression (not used))
- **escape_probability** (regression (not used))

For `survived_24h`, the pipeline uses:
1. Label encoding for categorical features (sex, level_id, special_rule)
2. Random undersampling to handle class imbalance
3. Hyperparameter tuning via GridSearchCV
4. XGBoost as the final model (best_model_v1.pkl)

## Deployment

### Docker (really recommended)

```bash
docker-compose up --build
```

- Backend: `http://localhost:8000` (FastAPI)
- Frontend: `http://localhost:8501` (Streamlit)

### Local

```bash
# Backend
pip install -r requirements-api.txt
uvicorn app.api.main:app --host 0.0.0.0 --port 8000

# Frontend
pip install -r requirements-ui.txt
streamlit run app/ui/main.py
```

## API

**POST** `/predict` (example)

```json
{
  "age": 25,
  "sex": "male",
  "height_cm": 175,
  "weight_kg": 70,
  "strength": 5,
  "reaction": 7,
  "stamina": 6,
  "speed": 5,
  "intelligence": 8,
  "perception": 6,
  "agility": 5,
  "endurance": 6,
  "stress_resistance": 7,
  "luck": 4,
  "panic": 30,
  "fatigue": 20,
  "hunger": 10,
  "thirst": 15,
  "mental_stability": 75,
  "focus": 70,
  "confidence": 60,
  "pain_tolerance": 50,
  "flashlight_battery": 66,
  "has_knife": 1,
  "medkit_count": 3,
  "water_amount": 3,
  "food_amount": 2,
  "has_radio": 0,
  "level_id": "6",
  "level_difficulty": 80,
  "visibility": 5,
  "entity_density": 50,
  "entity_aggression": 50,
  "resource_density": 20,
  "maze_complexity": 80,
  "geometry_stability": 70,
  "special_rule": "darkness",
  "spawn_area_danger": 45,
  "distance_to_nearest_entity": 30,
  "noise_generated": 25,
  "time_since_last_encounter": 4
}
```

Response (example too):
```json
{
  "prediction": 0,
  "probability": 0.387
}
```

<p align="center">
  <img src="https://img.shields.io/badge/BackroomsML-Survival%20Prediction-%232A8A3E?style=for-the-badge" alt="BackroomsML">
</p>
