import streamlit as st
import requests
import os
from custom_audio_player import custom_audio_player


API_BASE_URL = 'http://localhost:8000/api/'

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def fetch_random_music():
    response = requests.get(API_BASE_URL + 'music/random/')
    response.raise_for_status()
    return response.json()

random_track = fetch_random_music()

if random_track:
    custom_audio_player(random_track['file'], 'frontend/style.css')

load_css('frontend/style.css')
