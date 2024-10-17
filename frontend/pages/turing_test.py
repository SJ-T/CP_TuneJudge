import requests
import streamlit as st
import time
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

def submit_rating(song_id, rating):
    response = requests.post(API_BASE_URL + 'ratings/rate_song/', json={'song': song_id, 'rating': rating})
    response.raise_for_status()
    return response.json()


if 'random_track' not in st.session_state:
    st.session_state.random_track = fetch_random_music()

custom_audio_player(st.session_state.random_track['file'])

# Rating section
st.write("Do you think this music was generated by AI?")
rating = st.slider("Rate from 1 (Definitely Human) to 5 (Definitely AI)", 1, 5, 3)

rating_labels = {
    1: "Definitely Human",
    2: "Probably Human",
    3: "Unsure",
    4: "Probably AI",
    5: "Definitely AI"
}

st.write(f"Your rating: {rating} - {rating_labels[rating]}")

if st.button("Submit Rating"):
    try:
        result = submit_rating(st.session_state.random_track['id'], rating)
        st.success("Rating submitted successfully!")

        # Fetch a new song after successful submission
        time.sleep(1)  # Give user time to see the success message
        st.session_state.random_track = fetch_random_music()
        st.rerun()
    except requests.RequestException as e:
        st.error(f"Error submitting rating: {str(e)}")

if st.button("Skip to Next Song"):
    st.session_state.random_track = fetch_random_music()
    st.rerun()

load_css('frontend/style.css')
