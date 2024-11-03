import streamlit as st

from utils import load_css


st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_icon=':notes:')
load_css()

st.title('Tune Judge')

st.write("""
Welcome to my capstone project! This application allows you to:

1. Explore data analysis of classical and pop music features
2. Participate in a Turing test to identify AI-generated music

Use the sidebar to navigate between pages and explore the app's features.
""")
