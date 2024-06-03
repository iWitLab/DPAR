import streamlit as st


def post_registration():
    placeholder = st.empty()
    with placeholder.container():
        st.subheader("You successfully registered to the website")
        st.subheader("Please login to continue the study")

        def advance1():
            st.session_state['form_display'] = 'login'
            placeholder.empty()

        st.button("Login", on_click=advance1)


