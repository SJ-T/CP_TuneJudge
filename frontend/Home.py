import streamlit as st
import sys

from pathlib import Path
from utils import load_css

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
load_css()

st.title("Tune Judge")

st.write("""
Welcome to my capstone project! This application allows you to:

1. Participate in a Turing test to identify AI-generated music
2. Explore data analysis of classical and pop music features

Use the sidebar to navigate between pages and explore the app's features.
""")
