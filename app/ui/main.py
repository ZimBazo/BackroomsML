import streamlit as st
import pandas as pd
import os
import requests
from loguru import logger


fastapi_url = 'http://127.0.0.1:8000'

st.set_page_config(page_title='Backrooms 24h', layout='centered')

st.title('Backrooms survival predictor')
st.write('Визуализация и предсказание выживания в Закулисье')

with st.expander("Характеристики персонажа", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider('Возраст', 12, 80, 25)
        sex = st.selectbox('Пол', ['female', 'male', 'other'])
        height_cm = st.slider('Рост (см)', 140, 210, 175)
        weight_kg = st.slider('Вес (кг)', 35, 137, 70)
    with col2:
        strength = st.slider('Сила', 0, 10, 5)
        reaction = st.slider('Реакция', 0, 10, 5)
        stamina = st.slider('Выносливость', 0, 10, 5)
        speed = st.slider('Скорость', 0, 10, 5)
        intelligence = st.slider('Интеллект', 0, 10, 5)
        perception = st.slider('Восприятие', 0, 10, 5)
        agility = st.slider('Ловкость', 0, 10, 5)
        endurance = st.slider('Стойкость', 0, 10, 5)
        stress_resistance = st.slider('Стрессоустойчивость', 0, 10, 5)
        luck = st.slider('Удача', 0, 10, 5)

with st.expander("Состояние персонажа"):
    col1, col2 = st.columns(2)
    with col1:
        panic = st.slider('Паника', 0, 100, 20)
        fatigue = st.slider('Усталость', 0, 100, 20)
        hunger = st.slider('Голод', 0, 100, 20)
        thirst = st.slider('Жажда', 0, 100, 20)
    with col2:
        mental_stability = st.slider('Психическая стабильность', 0, 100, 80)
        focus = st.slider('Фокус', 0, 100, 80)
        confidence = st.slider('Уверенность', 0, 100, 80)
        pain_tolerance = st.slider('Терпимость к боли', 0, 100, 50)

with st.expander("Снаряжение"):
    col1, col2 = st.columns(2)
    with col1:
        has_flashlight = st.checkbox('Фонарик')
        flashlight_battery = st.slider('Заряд фонарика', 0, 100, 100)
        has_knife = st.checkbox('Нож')
        has_backpack = st.checkbox('Рюкзак')
    with col2:
        has_first_aid_kit = st.checkbox('Аптечка')
        medkit_count = st.slider('Количество аптечек', 0, 10, 1)
        has_water = st.checkbox('Вода')
        water_amount = st.slider('Количество воды (мл)', 0, 3000, 500)
        has_food = st.checkbox('Еда')
        food_amount = st.slider('Количество еды (ккал)', 0, 3000, 500)
        has_radio = st.checkbox('Рация')

with st.expander("Характеристики уровня"):
    col1, col2 = st.columns(2)
    with col1:
        level_id = st.selectbox('ID уровня', ['0', '1', '2', '3', '4', '5', '6', '7', '8', 'end'])
        level_difficulty = st.slider('Сложность уровня', 1, 5, 2)
        visibility = st.slider('Видимость', 0, 100, 80)
        entity_density = st.slider('Плотность сущностей', 0, 100, 20)
        entity_aggression = st.slider('Агрессия сущностей', 0, 100, 20)
    with col2:
        resource_density = st.slider('Плотность ресурсов', 0, 100, 50)
        maze_complexity = st.slider('Сложность лабиринта', 0, 100, 30)
        geometry_stability = st.slider('Стабильность геометрии', 0, 100, 90)
        special_rule = st.selectbox('Особое правило', ['neutral', 'liminal_office', 'mechanical_noise', 'haunted_hotel', 'cave_isolation', 'flooding', 'trap_exit', 'darkness'])
        spawn_area_danger = st.slider('Опасность зоны спавна', 0, 100, 10)
        distance_to_nearest_entity = st.slider('Расстояние до ближайшей сущности', 0, 100, 50)
        noise_generated = st.slider('Генерируемый шум', 0, 100, 20)
        time_since_last_encounter = st.slider('Время с последней встречи (ч)', 0, 24, 2)

if st.button('Предсказать выживаемость'):
    payload = {
        'age': age,
        'sex': sex,
        'height_cm': height_cm,
        'weight_kg': weight_kg,
        'strength': strength,
        'reaction': reaction,
        'stamina': stamina,
        'speed': speed,
        'intelligence': intelligence,
        'perception': perception,
        'agility': agility,
        'endurance': endurance,
        'stress_resistance': stress_resistance,
        'luck': luck,
        'panic': panic,
        'fatigue': fatigue,
        'hunger': hunger,
        'thirst': thirst,
        'mental_stability': mental_stability,
        'focus': focus,
        'confidence': confidence,
        'pain_tolerance': pain_tolerance,
        'has_flashlight': int(has_flashlight),
        'flashlight_battery': flashlight_battery,
        'has_knife': int(has_knife),
        'has_backpack': int(has_backpack),
        'has_first_aid_kit': int(has_first_aid_kit),
        'medkit_count': medkit_count,
        'has_water': int(has_water),
        'water_amount': water_amount,
        'has_food': int(has_food),
        'food_amount': food_amount,
        'has_radio': int(has_radio),
        'level_id': level_id,
        'level_difficulty': level_difficulty,
        'visibility': visibility,
        'entity_density': entity_density,
        'entity_aggression': entity_aggression,
        'resource_density': resource_density,
        'maze_complexity': maze_complexity,
        'geometry_stability': geometry_stability,
        'special_rule': special_rule,
        'spawn_area_danger': spawn_area_danger,
        'distance_to_nearest_entity': distance_to_nearest_entity,
        'noise_generated': noise_generated,
        'time_since_last_encounter': time_since_last_encounter
    }
    
    response = requests.post(f'{fastapi_url}/predict', json=payload)
    
    if response.status_code == 200:
        data = response.json()
        result = data.get("prediction")
        is_survived = ['Человек НЕ выжил', 'Человек выжил'][result]
        st.success(f'Результат: {is_survived}')
    else:
        st.error(f'Ошибка при запросе: {response.status_code}')

if st.button('Предсказать выживаемость'):
    response = requests.post(f'{fastapi_url}/predict', json={
        'fatigue': fatigue,
        'panic': panic,
        'thirst': thirst,
        'reaction': reaction,
        'hunger': hunger
    })

    data = response.json()
    data = data.get("prediction")
    is_survived = ['Человек НЕ выжил', 'Человек выжил'][data]
    st.write(is_survived)