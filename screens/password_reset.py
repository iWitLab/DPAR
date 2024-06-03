import streamlit as st


def reset():
    if authentication_status:
        try:
            if authenticator.reset_password(username, 'Reset password'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)