import streamlit as st
from screens.login_page import login
from screens.landing_page import landing
# from screens.landing_page_part_2 import landing
from screens.registration_page import register
from screens.registration_page2 import register2
from screens.on_app_load import app_loader
from screens.questionnaire import questionnaire
from screens.post_registration import post_registration
from screens.failed_login import failed_login
from screens.post_successful_login import successful_login


st.set_page_config(page_title='TAU IWiT Registration Form', layout='wide', page_icon='static/images/favicon-32x32.png',
                   initial_sidebar_state='auto')

st.markdown('''
        <style>
        .css-12ttj6m.epcbefy1 {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.25rem;
            padding: calc(1em - 1px);
        }
        .css-1cpxqw2.edgvbvh5 {
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 400;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            margin: 0px;
            line-height: 1.6;
            color: white;
            width: 100px;
            user-select: none;
            background-color: rgb(255, 255, 255);
            border-radius: 7px;
            border: 1px #015E92;
            background-image: linear-gradient(to bottom, #579add, #2773bd);
        }
        .css-1cpxqw2.edgvbvh9 {
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 400;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            margin: 0px;
            line-height: 1.6;
            color: white;
            width: 275px;
            user-select: none;
            background-color: rgb(255, 255, 255);
            border-radius: 7px;
            border: 1px #015E92;
            background-image: linear-gradient(to bottom, #579add, #2773bd);
        } 
        .css-kmrnrr.e1tzin5v4 {
            width: unset !important;
            background-color: #ffff;
            margin: auto;
            padding: 20px;
            margin-top: -100px;
            margin-left: -100px;
            margin-bottom: -200px;
            z-index: 1001;
            border-radius: 5px;
        }
        .css-g70r9e {
            width: unset !important;
            background-color: #ffff;
            margin: auto;
            padding: 20px;
            margin-top: -100px;
            margin-left: -100px;
            margin-bottom: -200px;
            z-index: 1001;
            border-radius: 5px;        
        }
        .css-1ufar69.e1tzin5v1 {
            padding: 30px;
            margin-top: -10px;
            margin-left: -500px;
            margin-bottom: -200px;
        }
        .lead {
            margin-bottom: 20px;
            font-size: 16px;
            font-weight: 300;
            line-height: 1.4
        }

        css.data-modal-container > :first-child > :first-child {
            # padding: 5px;
            width: unset !important;
            background-color: #f0f0f0;
            margin: auto;
            padding: 10px;
            margin-top: 10px;
            margin-left: 10px;
            margin-bottom: 10px;
            z-index: 1001;
            border-radius: 5px;
        }
        @media (min-width:768px) {
            .lead {
                font-size: 21px
            }
        }
        </style>''', unsafe_allow_html=True)

with open('static/css/bootstrap.min.css') as f:
    st.markdown(f'<style>(f.read())</style>', unsafe_allow_html=True)
app_loader()

if st.session_state['form_display'] == 'landing':
    landing()
if st.session_state['form_display'] == 'registration':
    register()
if st.session_state['form_display'] == 'register2':
    register2()
if st.session_state['form_display'] == 'post_registration':
    post_registration()
if st.session_state['form_display'] == 'login':
    login()
if st.session_state['form_display'] == 'failed_login':
    failed_login()
if st.session_state['form_display'] == 'successful_login':
    successful_login()
if st.session_state['form_display'] == 'questionnaire':
    questionnaire()
