from turtle import fillcolor

from pandas.core.config_init import val_mca
import streamlit as st
import pandas as pd
import os
import random
import requests
import plotly.graph_objects as go
from loguru import logger


fastapi_url = 'http://127.0.0.1:8000'

st.set_page_config(page_title='Backrooms 24h', layout='centered')

st.title('Backrooms survival predictor')
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Характеристики персонажа', 'Состояние персонажа', 'Снаряжение', 'Характеристики уровня', 'Предсказание'])

# State
if 'sex' not in st.session_state:
            st.session_state.sex = 'male'

if 'level_id' not in st.session_state:
            st.session_state.level_id = '0'

# Hooks
def sex_check():
    if st.session_state.sex != None:
        return 
    else:
        st.session_state.sex = 'male'
        # return

def level_check():
    if st.session_state.level_id != None:
        return 
    else:
        st.session_state.level_id = '0'
        # return

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider('Возраст', 12, 80, 25)
        sex = st.pills('Пол', ['female', 'male', 'other'], on_change=sex_check, key='sex')
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

# with st.expander("Характеристики персонажа", expanded=True):
    
with tab2:
    if st.button('Рандомизировать состояние', width='stretch'):
        st.session_state.panic = random.randint(0, 100)
        st.session_state.fatigue = random.randint(0, 100)
        st.session_state.hunger = random.randint(0, 100)
        st.session_state.thirst = random.randint(0, 100)
        st.session_state.mental_stability = random.randint(0, 100)
        st.session_state.focus = random.randint(0, 100)
        st.session_state.confidence = random.randint(0, 100)
        st.session_state.pain_tolerance = random.randint(0, 100)

    categories = ['Паника', 'Усталость', 'Голод', 'Жажда', 'Псих. стабильность', 'Фокус', 'Уверенность', 'Терпимость к боли']
    values = [
        st.session_state.get('panic', 20),
        st.session_state.get('fatigue', 20),
        st.session_state.get('hunger', 20),
        st.session_state.get('thirst', 20),
        st.session_state.get('mental_stability', 80),
        st.session_state.get('focus', 80),
        st.session_state.get('confidence', 80),
        st.session_state.get('pain_tolerance', 50),
    ]
    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Состояние',
        fillcolor='rgba(212, 175, 55, 0.3)',
        line=dict(color='#d4af37', width=2),
        marker=dict(size=5, color='#d4af37'),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            gridshape='linear',
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#3b382b', linecolor='#3b382b', tickfont=dict(color='#807c5a', size=11), ticksuffix=''),
            angularaxis=dict(gridcolor='#3b382b', linecolor='#3b382b', tickfont=dict(color='#e6dfb8', size=13)),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=30, b=30),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    panic = st.session_state.get('panic', 20)
    fatigue = st.session_state.get('fatigue', 20)
    hunger = st.session_state.get('hunger', 20)
    thirst = st.session_state.get('thirst', 20)
    mental_stability = st.session_state.get('mental_stability', 80)
    focus = st.session_state.get('focus', 80)
    confidence = st.session_state.get('confidence', 80)
    pain_tolerance = st.session_state.get('pain_tolerance', 50)

with tab3:
# with st.expander("Снаряжение"):
    col1, col2 = st.columns(2)
    with col1:
        has_flashlight = st.toggle('Фонарик')
        flashlight_battery = st.slider('Заряд фонарика', 0, 100, 100, disabled=(not has_flashlight))
        has_knife = st.toggle('Нож')
        has_backpack = st.toggle('Рюкзак')
    with col2:
        has_first_aid_kit = st.toggle('Аптечка')
        medkit_count = st.slider('Количество аптечек', 0, 10, 1, disabled=(not has_first_aid_kit))
        has_water = st.toggle('Вода')
        water_amount = st.slider('Количество воды (мл)', 0, 3000, 500, disabled=(not has_water))
        has_food = st.toggle('Еда')
        food_amount = st.slider('Количество еды (ккал)', 0, 3000, 500, disabled=(not has_food))
        has_radio = st.toggle('Рация')

with tab4:
# with st.expander("Характеристики уровня"):
    col1, col2 = st.columns(2)
    with col1:
        level_id = st.pills('ID уровня', ['0', '1', '2', '3', '4', '5', '6', '7', '8', 'end'], on_change=level_check, key='level_id', default='0')
        level_difficulty = st.slider('Сложность уровня', 1, 5, 2)
        visibility = st.slider('Видимость', 0, 100, 80)
        entity_density = st.slider('Плотность сущностей', 0, 100, 20)
        entity_aggression = st.slider('Агрессия сущностей', 0, 100, 20)
    with col2:
        resource_density = st.slider('Плотность ресурсов', 0, 100, 50)
        maze_complexity = st.slider('Сложность лабиринта', 0, 100, 30)
        geometry_stability = st.slider('Стабильность геометрии', 0, 100, 90)
        special_rule = st.selectbox('Особое правило', ['cave_isolation', 'darkness', 'flooding', 'haunted_hotel', 'liminal_office', 'mechanical_noise', 'neutral', 'resource_rich', 'trap_exit'])
        spawn_area_danger = st.slider('Опасность зоны спавна', 0, 100, 10)
        distance_to_nearest_entity = st.slider('Расстояние до ближайшей сущности', 0, 100, 50)
        noise_generated = st.slider('Генерируемый шум', 0, 100, 20)
        time_since_last_encounter = st.slider('Время с последней встречи (ч)', 0, 24, 2)

with tab5:

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
        'flashlight_battery': flashlight_battery if has_flashlight else 0,
        'has_knife': int(has_knife),
        'has_backpack': int(has_backpack),
        'has_first_aid_kit': int(has_first_aid_kit),
        'medkit_count': medkit_count if has_first_aid_kit else 0,
        'has_water': int(has_water),
        'water_amount': water_amount if has_water else 0,
        'has_food': int(has_food),
        'food_amount': food_amount if has_food else 0,
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

    if st.button('Предсказать выживаемость', width='stretch'):
        st.dataframe(payload)

        @st.dialog('Предсказание:')
        def prediction():
            response = requests.post(f'{fastapi_url}/predict', json=payload)
        
            if response.status_code == 200:
                data = response.json()
                result = data.get("prediction")
                is_survived = ['Человек НЕ выжил', 'Человек выжил'][result]
                st.success(f'Результат: {is_survived}')

                result = data.get("probability")
                surviving_probability = result
                st.success(f'Вероятность выживания: {surviving_probability:.3f}')
            else:
                st.error(f'Ошибка при запросе: {response.status_code}')

        prediction()