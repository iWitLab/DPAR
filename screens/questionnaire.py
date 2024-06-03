from bokeh.models.widgets import Div
import streamlit as st


def questionnaire():
    js = "window.location.href = 'https://en.wikipedia.org/wiki/Anonymous_(hacker_group)'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)
