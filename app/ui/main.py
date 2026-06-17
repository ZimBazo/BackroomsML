import streamlit as st
import pandas as pd
import os
import requests
from loguru import logger


fastapi_url = 'http://127.0.0.1:8000'

st.set_page_config(page_title='Backrooms 24h', layout='wide')

st.title('Backrooms survival predictor')
st.write('Визуализация и предсказание выживания в Закулисье')

name = st.text_input('Введите имя', max_chars=100)
surname = st.text_input('Введите фамилию', max_chars=100)
if st.button('Отправить на бекенд'):
    response = requests.post(f'{fastapi_url}/text-claim', json={'name': name, 'surname': surname})
    data = response.json()
    st.write(data.get('surname'))