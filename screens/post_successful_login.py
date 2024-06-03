import streamlit as st


def successful_login():
    placeholder = st.empty()
    with placeholder.container():
        st.subheader("You successfully logged in. Please remember your username and password")
        st.subheader("Please press questionnaire to complete the first phase of this study")

        def advance1():
            st.session_state['form_display'] = 'questionnaire'
            placeholder.empty()

        st.button("Questionnaire", on_click=advance1)


