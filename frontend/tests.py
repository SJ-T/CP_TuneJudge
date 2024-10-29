import pandas as pd
import pytest
import requests

from streamlit.testing.v1 import AppTest
from unittest.mock import patch, MagicMock
from utils import fetch_random_music, submit_rating, load_data

@pytest.fixture
def mock_random_track():
    return {'id': 1, 'title': 'Test Song', 'file': 'test.wav', 'label': 'pop'}

@pytest.fixture
def rating_payload():
    return {'song': 1, 'rating': 4}

@pytest.fixture
def mock_rating_response():
    return {'id': 1, 'song': 1, 'rating': 4, 'created_at': '2024-10-28T10:00:00Z'}

@pytest.fixture
def mock_analysis_data():
    return {
        'origin_df': pd.DataFrame({
            'genre': ['pop', 'classical'],
            'complexity': [5.0, 7.0],
            'originality': [6.0, 8.0]
        }).to_dict('records'),
        'pitch_class_dist': {
            'pop': [0.1] * 12,
            'classical': [0.08] * 12,
            'pitch_classes': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        }
    }

@pytest.fixture
def mock_features_data():
    return get_mock_data()
# test Home page
def test_home_page():
    at = AppTest.from_file('Home.py').run()
    assert not at.exception
    assert at.title[0].value == 'Tune Judge'
    assert "Use the sidebar" in at.markdown[1].value


# test Turing_Test page
@patch('utils.fetch_random_music')
def test_turing_test_page(mock_fetch_random_music, mock_random_track):
    mock_fetch_random_music.return_value = mock_random_track

    at = AppTest.from_file('pages/🎵_Turing_Test.py').run()
    assert not at.exception
    assert 'Do you think this track was generated by AI?' in at.markdown[1].value
    assert at.select_slider[0].label == 'Use the slider to rate from 1 (Definitely AI) to 5 (Definitely Human)'
    assert 'Your rating: 3 - Unsure' in at.markdown[2].value
    assert 'Submit Rating' in at.button[0].label
    assert 'Skip to Next Song' in at.button[1].label

@patch('utils.fetch_random_music')
@patch('utils.submit_rating')
def test_rating_submission(mock_submit_rating, mock_fetch_random_music, mock_random_track, mock_rating_response,
                           monkeypatch):
    monkeypatch.setattr('streamlit.rerun', lambda: None)
    mock_fetch_random_music.return_value = mock_random_track
    mock_submit_rating.return_value = mock_rating_response

    at = AppTest.from_file('pages/🎵_Turing_Test.py').run()
    at.select_slider[0].set_value(4).run()
    assert at.select_slider[0].value == 4
    assert 'Your rating: 4 - Probably Human' in at.markdown[2].value

    at.button[0].click().run()
    assert 'Rating submitted successfully!' in at.success[0].value
    assert 'Up next: Moving to the next track...' in at.info[0].value

@patch('utils.fetch_random_music')
@patch('utils.submit_rating')
def test_rating_submission_error(mock_submit_rating, mock_fetch_random_music, mock_random_track):
    mock_fetch_random_music.return_value = mock_random_track
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {'error': 'Invalid request'}
    mock_submit_rating.side_effect = requests.HTTPError(response=mock_response)

    at = AppTest.from_file('pages/🎵_Turing_Test.py').run()
    at.button[0].click().run()
    assert 'Invalid request' in at.error[0].value

@patch('utils.fetch_random_music')
@patch('utils.submit_rating')
def test_rating_submission_404(mock_submit_rating, mock_fetch_random_music, mock_random_track, monkeypatch):
    monkeypatch.setattr('streamlit.rerun', lambda: None)
    mock_fetch_random_music.return_value = mock_random_track
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {'error': 'Song not found'}
    mock_submit_rating.side_effect = requests.HTTPError(response=mock_response)

    at = AppTest.from_file('pages/🎵_Turing_Test.py').run()
    at.button[0].click().run()
    assert 'Song not found' in at.error[0].value

@patch('utils.fetch_random_music')
def test_skip_song(mock_fetch_random_music, mock_random_track):
    mock_fetch_random_music.return_value = mock_random_track
    at = AppTest.from_file('pages/🎵_Turing_Test.py').run()
    at.button[1].click().run()
    assert at.session_state['random_track'] == mock_random_track


# test endpoint
@patch('requests.get')
def test_fetch_random_music_endpoint(mock_get, mock_random_track):
    mock_get.return_value.json.return_value = mock_random_track

    result = fetch_random_music()
    assert result == mock_random_track

@patch('requests.post')
def test_submit_rating_endpoint(mock_post, rating_payload, mock_rating_response):
    mock_post.return_value.json.return_value = mock_rating_response

    result = submit_rating(rating_payload['song'], rating_payload['rating'])
    assert result == mock_rating_response

@patch('requests.get')
def test_load_data(mock_get, mock_analysis_data):
    mock_get.return_value.json.return_value = mock_analysis_data

    result = load_data()
    assert 'origin_df' in result
    assert 'pitch_class_dist' in result
    assert isinstance(result['origin_df'], pd.DataFrame)
