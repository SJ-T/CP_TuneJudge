import streamlit as st
import requests

API_BASE_URL = 'http://localhost:8000/api/'


def fetch_data(end_point):
    response = requests.get(end_point)
    response.raise_for_status()
    return response.json()


music_data = fetch_data(API_BASE_URL + 'music')

# st.write(music_data)
for track in music_data:
    st.write(track['title'])
    st.audio(track['file'])

