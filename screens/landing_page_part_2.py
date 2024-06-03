import streamlit as st
from PIL import Image


def landing():
    registration_1 = st.empty()
    c = registration_1.container()
    with c.container():
        image = Image.open("static/images/bobo1.png")
        st.image(image)
        texto = '''<p class="lead">Thank you for returning to the second part of this study. <br> 
        Please login to our application and complete the survey. <br>
        '''

        st.markdown(texto, unsafe_allow_html=True)

        if st.button('Login'):
            st.session_state['form_display'] = 'login'
            registration_1.empty()
            return True