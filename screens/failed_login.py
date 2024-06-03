import streamlit as st


def failed_login():
    placeholder = st.empty()
    with placeholder.container():
        st.subheader("Login failed, following 5 unsuccessful login attempts")
        st.subheader("Please press questionnaire to complete the first phase of this study")

        def advance1():
            st.session_state['form_display'] = 'questionnaire'
            placeholder.empty()

        st.button("Questionnaire", on_click=advance1)


