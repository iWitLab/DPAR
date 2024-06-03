import streamlit as st
import json
from PIL import Image
import hashlib
import time
import datetime


def landing():
    registration_1 = st.empty()
    c = registration_1.container()
    with c.container():
        image = Image.open("static/images/bobo1.png")
        st.image(image)
        texto = '''<p class="lead">This is an experiment on people reactions to website registration processes. <br> 
        In this experiment you will be asked to create a username and a password for yourself. <br> 
        Please imagine that this is a significant account that carries sensitive information (for instance bank account or health information). <br>
        Next, you'll be asked to login to our system and fill out a basic survey. <br>
        Two days later you'll be asked to login again and complete the survey. <br>
        Please note that the survey is confidential and anonymized according to guidelines from our ethics review board.</p><br>'''



        st.markdown(texto, unsafe_allow_html=True)

        if st.button('Login'):
            st.session_state['form_display'] = 'registration'
            registration_1.empty()
            return True