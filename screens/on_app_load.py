import streamlit as st
import json
import extra_streamlit_components as stx
from random import randrange
import time
import os

os.environ['MY_REGION'] = ''
os.environ['MY_KEY_ENV'] = ''
os.environ['MY_SECRET_ENV'] = ''

def app_loader():
    def get_manager():
        return stx.CookieManager()
    cookie_manager = get_manager()

    if 'experiment_group' not in st.session_state:
        st.session_state['experiment_group'] = randrange(4) + 1
    if 'cookies' not in st.session_state:
        st.session_state['cookies'] = cookie_manager.get_all()
    if 'username_value' not in st.session_state:
        st.session_state['username_value'] = ''
    if 'password_value' not in st.session_state:
        st.session_state['password_value'] = ''
    if 'password2_value' not in st.session_state:
        st.session_state['password2_value'] = ''
    if 'recommendation_button_pressed' not in st.session_state:
        st.session_state['recommendation_button_pressed'] = 0
    if 'password_flag' not in st.session_state:
        st.session_state['password_flag'] = False
    if 'failed_logins_user' not in st.session_state:
        st.session_state['failed_logins_user'] = 0
    if 'failed_logins_password' not in st.session_state:
        st.session_state['failed_logins_password'] = 0
    if 'users' not in st.session_state:
        f = open('output/users.json', "r")
        st.session_state['users'] = json.loads(f.read())
    if 'form_display' not in st.session_state:
        st.session_state['form_display'] = 'landing'
    if 'watched_recom_1' not in st.session_state:
        st.session_state['watched_recom_1'] = False
    if 'watched_recom_2' not in st.session_state:
        st.session_state['watched_recom_2'] = False
    if 'watched_recom_3' not in st.session_state:
        st.session_state['watched_recom_3'] = False
    if 'chosen_recommendation' not in st.session_state:
        st.session_state['chosen_recommendation'] = 0
    if 'register_1_password' not in st.session_state:
        st.session_state['register_1_password'] = ''
    if 'register_2_password' not in st.session_state:
        st.session_state['register_2_password'] = ''
    if 'form_inject' not in st.session_state:
        st.session_state['form_inject'] = randrange(2) + 1
    if 'registration1_start_time' not in st.session_state:
        st.session_state['registration1_start_time'] = time.time()
    if 'MY_REGION' not in st.session_state:
        st.session_state['MY_REGION'] = os.getenv('MY_REGION')
    if 'MY_KEY_ENV' not in st.session_state:
        st.session_state['MY_KEY_ENV'] = os.getenv('MY_KEY_ENV')
    if 'MY_SECRET_ENV' not in st.session_state:
        st.session_state['MY_SECRET_ENV'] = os.getenv('MY_SECRET_ENV')
    if 'missing_value' not in st.session_state:
        st.session_state['missing_value'] = 'missing_value'
    if 'recommendation_button_1_pressed' not in st.session_state:
        st.session_state['recommendation_button_1_pressed'] = 0
    if 'recommendation_button_2_pressed' not in st.session_state:
        st.session_state['recommendation_button_2_pressed'] = 0
    if 'recommendation_button_3_pressed' not in st.session_state:
        st.session_state['recommendation_button_3_pressed'] = 0
    if 'recommendation_1_injected' not in st.session_state:
        st.session_state['recommendation_1_injected'] = 0
    if 'recommendation_2_injected' not in st.session_state:
        st.session_state['recommendation_2_injected'] = 0
    if 'recommendation_3_injected' not in st.session_state:
        st.session_state['recommendation_3_injected'] = 0
    if 'recommendation_1_canceled' not in st.session_state:
        st.session_state['recommendation_1_canceled'] = 0
    if 'recommendation_2_canceled' not in st.session_state:
        st.session_state['recommendation_2_canceled'] = 0
    if 'recommendation_3_canceled' not in st.session_state:
        st.session_state['recommendation_3_canceled'] = 0
    if 'second_shown' not in st.session_state:
        st.session_state['second_shown'] = 0

