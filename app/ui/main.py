import streamlit as st
import pandas as pd
import os
import requests
from loguru import logger


fastapi_url = 'http://127.0.0.1:8000'

st.set_page_config(page_title='Backrooms 24h', layout='centered')

st.title('Backrooms survival predictor')
st.write('Визуализация и предсказание выживания в Закулисье')

fatigue = st.slider('Усталость', min_value=0, max_value=100)
panic = st.slider('Паника', min_value=0, max_value=100)
thirst = st.slider('Жажда', min_value=0, max_value=100)
reaction = st.slider('Реакция', min_value=0, max_value=10)
hunger = st.slider('Голод', min_value=0, max_value=100)

# dataframe_for_pydantic = df_temp[['fatigue', 'panic', 'thirst', 'reaction', 'hunger', 'survived_24h']]

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