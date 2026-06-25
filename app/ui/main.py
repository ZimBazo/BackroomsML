from pandas.core.config_init import val_mca
import streamlit as st
import pandas as pd
import os
import random
import requests
import plotly.graph_objects as go
# from loguru import logger


# fastapi_url = 'http://127.0.0.1:8000'
fastapi_url = os.environ.get('API_URL', 'http://127.0.0.1:8000')

LEVEL_PRESETS = {
    '0':  {'level_difficulty': 60, 'visibility': 65, 'entity_density': 15, 'entity_aggression': 10, 'resource_density': 30, 'maze_complexity': 85, 'geometry_stability': 60, 'special_rule': 'neutral'},
    '1':  {'level_difficulty': 40, 'visibility': 70, 'entity_density': 25, 'entity_aggression': 15, 'resource_density': 55, 'maze_complexity': 50, 'geometry_stability': 75, 'special_rule': 'neutral'},
    '2':  {'level_difficulty': 70, 'visibility': 40, 'entity_density': 35, 'entity_aggression': 30, 'resource_density': 25, 'maze_complexity': 75, 'geometry_stability': 50, 'special_rule': 'mechanical_noise'},
    '3':  {'level_difficulty': 75, 'visibility': 50, 'entity_density': 40, 'entity_aggression': 35, 'resource_density': 30, 'maze_complexity': 70, 'geometry_stability': 55, 'special_rule': 'mechanical_noise'},
    '4':  {'level_difficulty': 30, 'visibility': 85, 'entity_density': 10, 'entity_aggression': 10, 'resource_density': 80, 'maze_complexity': 30, 'geometry_stability': 90, 'special_rule': 'liminal_office'},
    '5':  {'level_difficulty': 65, 'visibility': 60, 'entity_density': 45, 'entity_aggression': 40, 'resource_density': 40, 'maze_complexity': 60, 'geometry_stability': 65, 'special_rule': 'haunted_hotel'},
    '6':  {'level_difficulty': 80, 'visibility': 5,  'entity_density': 50, 'entity_aggression': 50, 'resource_density': 20, 'maze_complexity': 80, 'geometry_stability': 70, 'special_rule': 'darkness'},
    '7':  {'level_difficulty': 75, 'visibility': 20, 'entity_density': 35, 'entity_aggression': 30, 'resource_density': 25, 'maze_complexity': 65, 'geometry_stability': 40, 'special_rule': 'flooding'},
    '8':  {'level_difficulty': 85, 'visibility': 30, 'entity_density': 45, 'entity_aggression': 45, 'resource_density': 20, 'maze_complexity': 90, 'geometry_stability': 30, 'special_rule': 'cave_isolation'},
    'end': {'level_difficulty': 90, 'visibility': 80, 'entity_density': 5,  'entity_aggression': 5,  'resource_density': 70, 'maze_complexity': 20, 'geometry_stability': 95, 'special_rule': 'trap_exit'},
}

LEVEL_IMAGES = {
    '0': 'app/ui/images/level_0.png',
    '1': 'app/ui/images/level_1.jpg',
    '2': 'app/ui/images/level_2.jpg',
    '3': 'app/ui/images/level_3.jpg',
    '4': 'app/ui/images/level_4.jpg',
    '5': 'app/ui/images/level_5.jpg',
    '6': 'app/ui/images/level_6.webp',
    '7': 'app/ui/images/level_7.webp',
    '8': 'app/ui/images/level_8.png',
    'end': 'app/ui/images/level_end.jpg',
}

st.set_page_config(page_title='Backrooms 24h', layout='centered')

st.image(image='app/ui/images/hero_image_3.png', width='stretch')  
# st.title('Backrooms survival predictor')
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Характеристики', 'Состояние', 'Снаряжение', 'Уровень', 'Предсказание'])


# State
if 'sex' not in st.session_state:
            st.session_state.sex = 'male'

if 'level_id' not in st.session_state:
            st.session_state.level_id = '0'

for key in ['flashlight_battery', 'food_amount', 'medkit_count', 'water_amount', 'has_knife', 'has_radio']:
    if f'{key}' not in st.session_state:
            st.session_state[f'{key}'] = 0

stats_defaults = {
    'strength': 5, 'reaction': 5, 'stamina': 5, 'speed': 5,
    'intelligence': 5, 'perception': 5, 'agility': 5, 'endurance': 5,
    'stress_resistance': 5, 'luck': 5
}
for stat, default in stats_defaults.items():
    if stat not in st.session_state:
        st.session_state[stat] = default

# Funcitons
def apply_level_preset():
    preset = LEVEL_PRESETS.get(st.session_state.level_id, {})
    for key, value in preset.items():
        st.session_state[key] = value

def sex_check():
    if st.session_state.sex != None:
        return 
    else:
        st.session_state.sex = 'male'

def stat_check():
    for stat in stats_defaults:
        if st.session_state.get(stat) is None:
            st.session_state[stat] = stats_defaults[stat]

def level_check():
    if st.session_state.level_id != None:
        apply_level_preset()
    else:
        st.session_state.level_id = '0'
        apply_level_preset()

def value_check(type: str):
    if st.session_state[f'{type}'] != None:
        return
    else:
        st.session_state[f'{type}'] = 0
        

with tab1:
    col1, col2 = st.columns([1, 1.58], width='stretch')
    with col1:
        name = st.text_input('Имя персонажа', placeholder='Введите имя персонажа')
        if 'name' not in st.session_state:
            st.session_state.name = name
        age = st.slider('Возраст', 12, 80, 25)
        sex = st.pills('Пол', ['female', 'male', 'other'], on_change=sex_check, key='sex')
        height_cm = st.slider('Рост (см)', 140, 210, 175)
        weight_kg = st.slider('Вес (кг)', 35, 137, 70)
            
    with col2:
        strength = st.segmented_control('Сила', list(range(1, 11)), on_change=stat_check, key='strength')
        reaction = st.segmented_control('Реакция', list(range(1, 11)), on_change=stat_check, key='reaction')
        stamina = st.segmented_control('Выносливость', list(range(1, 11)), on_change=stat_check, key='stamina')
        speed = st.segmented_control('Скорость', list(range(1, 11)), on_change=stat_check, key='speed')
        intelligence = st.segmented_control('Интеллект', list(range(1, 11)), on_change=stat_check, key='intelligence')
        perception = st.segmented_control('Восприятие', list(range(1, 11)), on_change=stat_check, key='perception')
        agility = st.segmented_control('Ловкость', list(range(1, 11)), on_change=stat_check, key='agility')
        endurance = st.segmented_control('Стойкость', list(range(1, 11)), on_change=stat_check, key='endurance')
        stress_resistance = st.segmented_control('Стрессоустойчивость', list(range(1, 11)), on_change=stat_check, key='stress_resistance')
        luck = st.segmented_control('Удача', list(range(1, 11)), on_change=stat_check, key='luck')

# with st.expander("Характеристики персонажа", expanded=True):
    
@st.fragment
def state_tab2():
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

with tab2:
    state_tab2()

with tab3:
    MAX_POINTS = 3

    used_points = sum([
        st.session_state.get('has_knife', 0),
        st.session_state.get('has_radio', 0),
        st.session_state.get('flashlight_battery', 0),
        st.session_state.get('medkit_count', 0),
        st.session_state.get('water_amount', 0),
        st.session_state.get('food_amount', 0),
    ])
    remaining = MAX_POINTS - used_points

    st.info(f"**Система очков:** У вас **{MAX_POINTS}** очков. "
            f"Каждый предмет или порция расходников стоит **1** очко. "
            f"Нож и рация — по 1 очку. Батарейки, аптечки, вода и еда — по 1 очку за порцию.")

    if remaining < 0:
        st.error(f'Превышен лимит очков! Потрачено: {used_points}, доступно: {MAX_POINTS}')
    elif remaining == 0:
        st.warning('Все очки потрачены!')
    else:
        st.metric('Оставшиеся очки', remaining)

    col1, col2 = st.columns(2)
    with col1:
        has_knife = st.segmented_control('Нож', [0, 1], key='has_knife')
        has_radio = st.segmented_control('Рация', [0, 1], key='has_radio')
        flashlight_battery = st.segmented_control('Батарейки фонарика', [0, 1, 2, 3], key='flashlight_battery')
    with col2:
        medkit_count = st.segmented_control('Аптечки', [0, 1, 2, 3], key='medkit_count')
        water_amount = st.segmented_control('Вода (500мл порции)', [0, 1, 2, 3], key='water_amount')
        food_amount = st.segmented_control('Еда (500ккал порции)', [0, 1, 2, 3], key='food_amount')

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        level_names = {
            '0': 'Level 0: Threshold',
            '1': 'Level 1: Habitable Zone',
            '2': 'Level 2: Abandoned Utility Halls',
            '3': 'Level 3: Electrical Station',
            '4': 'Level 4: Abandoned Office',
            '5': 'Level 5: Terror Hotel',
            '6': 'Level 6: Lights Out',
            '7': 'Level 7: Flooded Sewers',
            '8': 'Level 8: Cave Systems',
            'end': 'The End: Trap level'
        }
        level_id = st.pills('Уровень', ['0', '1', '2', '3', '4', '5', '6', '7', '8', 'end'], on_change=level_check, key='level_id', default='0', format_func=lambda x: level_names.get(x, x))
    with col2:
        st.image(image=LEVEL_IMAGES.get(st.session_state.level_id), width='stretch')    
        with st.expander('Характеристики уровня'):   
            level_difficulty = st.slider('Сложность уровня', 0, 100, st.session_state.get('level_difficulty', 60), disabled=True)
            visibility = st.slider('Видимость', 0, 100, st.session_state.get('visibility', 65), disabled=True)
            entity_density = st.slider('Плотность сущностей', 0, 100, st.session_state.get('entity_density', 15), disabled=True)
            entity_aggression = st.slider('Агрессия сущностей', 0, 100, st.session_state.get('entity_aggression', 10), disabled=True)
            resource_density = st.slider('Плотность ресурсов', 0, 100, st.session_state.get('resource_density', 30), disabled=True)
            maze_complexity = st.slider('Сложность лабиринта', 0, 100, st.session_state.get('maze_complexity', 85), disabled=True)
            geometry_stability = st.slider('Стабильность геометрии', 0, 100, st.session_state.get('geometry_stability', 60), disabled=True)
            special_rule = st.selectbox('Особое правило', ['cave_isolation', 'darkness', 'flooding', 'haunted_hotel', 'liminal_office', 'mechanical_noise', 'neutral', 'resource_rich', 'trap_exit'], index=['cave_isolation', 'darkness', 'flooding', 'haunted_hotel', 'liminal_office', 'mechanical_noise', 'neutral', 'resource_rich', 'trap_exit'].index(st.session_state.get('special_rule', 'neutral')), disabled=True)
            st.info('Помимо этих характеристик, каждый уровень несет в себе скрытый признак, который такжже влияет на предсказание')
        with st.expander('Ситуативные характеристики', expanded=True): 
            spawn_area_danger = st.slider('Опасность зоны спавна', 0, 100, st.session_state.get('spawn_area_danger', 10))
            distance_to_nearest_entity = st.slider('Расстояние до ближайшей сущности', 0, 100, st.session_state.get('distance_to_nearest_entity', 50))
            noise_generated = st.slider('Генерируемый шум', 0, 100, st.session_state.get('noise_generated', 20))
            time_since_last_encounter = st.slider('Время с последней встречи (ч)', 0, 24, st.session_state.get('time_since_last_encounter', 2))

good_messages = {
    '1': 'пережил ещё один день в бесконечных жёлтых комнатах.',
    '2': 'нашёл бутылку настоящей миндальной воды и выжил.',
    '3': 'успешно спрятался от Смайлера.',
    '4': f'пережил ночь на {st.session_state.level_id}',
    '5': f'выбрался из сырого подвала Уровня {st.session_state.level_id} живым.',
    '6': 'не сошёл с ума от гула ламп за целый день.',
    '7': 'сумел убежать от Гончей.',
    '8': 'нашёл относительно безопасную комнату и отдохнул.',
    '9': 'пережил встречу с Partygoer\'ом и остался цел.',
    '10': 'прошёл через тёмный коридор и увидел свет (ламп).',
    '11': 'прожил день без единого noclip\'а.',
    '12': 'нашёл выход... на следующий уровень.',
    '13': 'не утонул в фальшивой миндальной воде.',
    '14': 'пережил обвал потолка и продолжил путь.',
    '15': 'наконец-то выспался под гулом флуоресцентных ламп.'
}

bad_messages = {
    '1': 'слишком сильно noclipped и провалился в Пустоту.',
    '2': f'был съеден заживо Смайлером на Уровне {st.session_state.level_id}',
    '3': 'пытался убежать от Гончей и не успел.',
    '4': 'потерялся навсегда в бесконечных жёлтых комнатах.',
    '5': f'был раздавлен обвалившимся бетоном на Уровне {st.session_state.level_id}',
    '6': 'слишком долго смотрел в темноту.',
    '7': 'утонул в «миндальной воде», которая оказалась чем-то другим.',
    '8': 'попал на неправильную вечеринку и был разорван Partygoers ;(',
    '9': 'провалился сквозь пол и исчез навсегда.',
    '10': 'наконец понял, что выхода нет.',
    '11': 'был убит Сущностью.',
    '12': 'решил срезать путь через "Уровень !".',
    '13': 'был пронзён ржавой арматурой в технических коридорах.',
    '14': 'сгорел заживо под бесконечными лампами.',
    '15': 'услышал шаги позади и больше ничего не услышал.'
}

def random_message(type: str):
    random_number = random.randint(1, 15)

    if type == 'good':
        return good_messages[f'{random_number}']
    elif type == 'bad':
        return bad_messages[f'{random_number}']

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
        'panic': st.session_state.get('panic', 20),
        'fatigue': st.session_state.get('fatigue', 20),
        'hunger': st.session_state.get('hunger', 20),
        'thirst': st.session_state.get('thirst', 20),
        'mental_stability': st.session_state.get('mental_stability', 80),
        'focus': st.session_state.get('focus', 80),
        'confidence': st.session_state.get('confidence', 80),
        'pain_tolerance': st.session_state.get('pain_tolerance', 50),
        # 'has_flashlight': int(has_flashlight),
        'flashlight_battery': (st.session_state.get('flashlight_battery', 0) * 33),
        'has_knife': st.session_state.get('has_knife', 0),
        # 'has_backpack': int(has_backpack),
        # 'has_first_aid_kit': int(has_first_aid_kit),
        'medkit_count': (st.session_state.get('medkit_count', 0) * 3),
        # 'has_water': int(has_water),
        'water_amount': (st.session_state.get('water_amount', 0) * 1000),
        # 'has_food': int(has_food),
        'food_amount': (st.session_state.get('food_amount', 0) * 1000),
        'has_radio': st.session_state.get('has_radio', 0),
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
    st.image(image='app/ui/images/predict_picture.webp', width='stretch')    
    if st.button('Предсказать выживаемость', width='stretch'):
        if remaining >= 0:
            @st.dialog('Предсказание:')
            def prediction():
                response = requests.post(f'{fastapi_url}/predict', json=payload)
            
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("prediction")
                    is_survived = [f'Неудача! Бедолага {name} {random_message(type="bad")}', f'Ура! Бедолага {name} {random_message(type="good")}'][result]
                    st.write(f'{is_survived}')
                    result = data.get("probability")
                    surviving_probability = result
                    st.badge(f'Вероятность выживания: {surviving_probability:.3f}', color='primary')
                else:
                    st.error(f'Ошибка при запросе: {response.status_code}')

            prediction()
        else:
            st.error('Вы потратили больше очков чем полагается!')

    st.table(payload)