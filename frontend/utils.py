import pandas as pd
import requests
import streamlit as st

from config import API_BASE_URL


def load_css(file_path='frontend/static/style.css'):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache_data
def load_music_data():
    return pd.read_csv('frontend/data/midi_ds_features.csv')


def fetch_random_music():
    response = requests.get(f"{API_BASE_URL}music/random/")
    response.raise_for_status()
    return response.json()


def submit_rating(song_id, rating):
    response = requests.post(f"{API_BASE_URL}ratings/rate_song/", json={'song': song_id, 'rating': rating})
    response.raise_for_status()
    return response.json()
