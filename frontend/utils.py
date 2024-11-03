import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

from config import API_BASE_URL


def load_css(file_path='static/style.css'):
    """
    Loads and applies custom CSS styling to the Streamlit application.
    Args:
        file_path (str): Path to the CSS file
    """
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# data analysis
def change_container_width(percentage: int):
    """
    Adjusts the width of the main container in Streamlit.
    Args:
        percentage (int): Desired width as percentage of viewport
    """
    css = f"""
    <style>
    .stMainBlockContainer {{
        max-width: {percentage}%;
        margin: 0 auto;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def no_header():
    """
    Removes the default Streamlit header from the application using CSS.
    """
    css = """
        <style>
            .stApp > header {
                display: none;
            }
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)


@st.cache_data
def load_data():
    """
    Fetches and processes music analysis data from the API.
    Uses Streamlit caching for performance.
    Returns:
        tuple: (processed_data, error_message)
            - processed_data: Dictionary of processed music data if successful
            - error_message: Error description if fetch fails
    """
    try:
        response = requests.get(f'{API_BASE_URL}feature-analysis/')
        data = response.json()
        if 'error' in data:
            return None, f"Error loading data: {data['error']}"

        df_dict = {}
        for key, value in data.items():
            if key in ['origin_df', 'pitch_class_dist', 'interval_dist', 'interval_size_dist', 'interval_dir_dist']:
                df_dict[key] = pd.DataFrame(value)
            elif key in ['pitch_transition_dist', 'interval_transition_dist']:
                df_dict[key] = {
                    genre: pd.DataFrame(data) for genre, data in value.items() if genre != 'labels'
                }
                df_dict[key]['labels'] = value['labels']
            else:
                df_dict[key] = value
        return df_dict, None
    except requests.ConnectionError:
        return None, 'Could not connect to the server.'
    except requests.Timeout:
        return None, 'Request timed out. Please try again.'
    except requests.RequestException as e:
        return None, f'Error fetching data: {str(e)}'


def plot_histogram(df: pd.DataFrame, x_col, title, xaxis_title=None, color=None, histnorm='probability', **kwargs):
    """
    Creates an interactive histogram using Plotly and displays it in Streamlit.
    Default normalization shows probability distribution rather than raw counts.
    Args:
        df: Pandas DataFrame containing the data to plot
        x_col: Name of the column to plot on x-axis
        title: Title of the histogram
        xaxis_title (optional): Custom x-axis label. If None, uses x_col name
        color (optional): Column name for color grouping
        histnorm (str): Histogram normalization method (default: 'probability')
        **kwargs: Additional Plotly Express histogram parameters
    """
    fig = px.histogram(df, x=x_col, title=title, color=color, histnorm=histnorm, **kwargs)
    if xaxis_title:
        fig.update_layout(xaxis_title=xaxis_title)
    st.plotly_chart(fig)


def plot_bar(df: pd.DataFrame, x_axis, y_axis, title, color, **kwargs):
    """
    Creates an interactive bar chart using Plotly and displays it in Streamlit.
    Can show either single series or grouped bars based on parameters.
    Args:
        df: Pandas DataFrame containing the data to plot
        x_axis: Name of the column for x-axis categories
        y_axis: Name of the column for y-axis values
        title: Title of the bar chart
        color: List of colors or column name for color grouping
        **kwargs: Additional parameters:
            - x_label: Custom x-axis label
            - sort: Whether to sort bars by value (default: True)
            - tick_labels: Custom tick labels for x-axis
            - color_map: Custom color mapping for categories
    """
    x_label = kwargs.get('x_label', x_axis)
    sort = kwargs.get('sort', True)
    tick_labels = kwargs.get('tick_labels', None)
    labels = {y_axis: 'probability', x_axis: x_label}
    if sort:
        fig = px.bar(df, x=x_axis, y=y_axis, color_discrete_sequence=color, title=title,
                     labels=labels,
                     category_orders={x_axis: df.sort_values(y_axis, ascending=False)[x_axis]})
    else:
        fig = px.bar(df, x=x_axis, y=y_axis, color=color, title=title, barmode='group',
                     labels=labels,
                     color_discrete_map=kwargs.get('color_map', None))
    if tick_labels:
        fig.update_xaxes(tickvals=list(range(len(tick_labels))), ticktext=list(tick_labels))
    st.plotly_chart(fig)


def plot_transition_heatmap(df: pd.DataFrame, color_scale, title, **kwargs):
    """
    Creates an interactive heatmap for transition matrices using Plotly.
    Useful for visualizing probabilities of transitions between musical elements.
    Args:
        df: DataFrame containing transition matrix data with 'data', 'columns', and 'index'
        color_scale: Color scheme for the heatmap (e.g., 'Blues', 'Oranges')
        title: Title of the heatmap
        **kwargs: Additional parameters:
            - tick_labels: Custom tick labels for both axes
    """
    tick_labels = kwargs.get('tick_labels', None)
    matrix_data = np.array([row for row in df['data']])
    fig = go.Figure(data=go.Heatmap(z=matrix_data, x=df['columns'], y=df['index'], colorscale=color_scale))
    fig.update_layout(title=title)
    if tick_labels:
        fig.update_xaxes(tickvals=list(range(len(tick_labels))), ticktext=list(tick_labels))
        fig.update_yaxes(tickvals=list(range(len(tick_labels))), ticktext=list(tick_labels)[::-1])
    st.plotly_chart(fig)


def plot_pie(df: pd.DataFrame, label: str, value: str, **kwargs):
    """
    Creates an interactive pie chart using Plotly and displays it in Streamlit.
    Includes hover information showing counts and percentages.
    Args:
        df: Pandas DataFrame containing the data to plot
        label: Name of the column for slice labels
        value: Name of the column for slice values
        **kwargs: Additional parameters:
            - title: Title of the pie chart
    """
    colors = ['gold', 'lightgreen']
    fig = go.Figure(
        data=[go.Pie(labels=df[label], values=df[value], textfont_size=20, title=kwargs.get('title'),
                     marker=dict(colors=colors, pattern=dict(shape=['.', 'x'])),
                     hovertemplate='%{label}<br>count: %{value}<br>%{percent}<extra></extra>')])
    st.plotly_chart(fig)


def classify_key_type(df: pd.DataFrame):
    """
    Categorizes musical pieces into major and minor keys and counts their distribution.
    Uses capitalization to distinguish between major keys (uppercase) and minor keys (lowercase).
    For example, 'C' is C major while 'c' is C minor.
    Args:
        df: Pandas DataFrame containing a 'key' column with musical key information
    Returns:
        DataFrame: Contains two columns:
            - key_type: Labels for 'Major' and 'Minor'
            - count: Number of pieces in each key type
    """
    major_keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    minor_keys = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    key_dist = pd.DataFrame({
        'key_type': ['Major', 'Minor'],
        'count': [
            df['key'].isin(major_keys).sum(),
            df['key'].isin(minor_keys).sum()
        ]
    })
    return key_dist


# turing test
def fetch_random_music():
    """
    Fetches a random music track from the API.
    Returns:
        tuple: (track_data, error_message)
            - track_data: Dictionary of track information if successful
            - error_message: Error description if fetch fails
    """
    try:
        response = requests.get(f'{API_BASE_URL}music/random/')
        if response.status_code == 200:
            return response.json(), None
        error = response.json()
        error_message = error.get('error', 'Unknown error occurred')
        return None, f'Server returned error {response.status_code}: {error_message}'
    except requests.ConnectionError:
        return None, 'Could not connect to the server.'
    except requests.Timeout:
        return None, 'Request timed out. Please try again.'
    except requests.RequestException as e:
        return None, f'Error fetching track: {str(e)}'


def submit_rating(song_id, rating):
    """
    Submits a rating for a music track to the API.
    Args:
        song_id: ID of the rated song
        rating: Rating value (1-5)
    Returns:
        tuple: (response_data, error_message)
            - response_data: Response from server if successful
            - error_message: Error description if submission fails
    """
    try:
        response = requests.post(f'{API_BASE_URL}ratings/rate_song/', json={'song': song_id, 'rating': rating})
        if response.status_code == 201:
            return response.json(), None
        error = response.json()
        error_message = error.get('error', 'Unknown error occurred')
        return None, f'Server returned error {response.status_code}: {error_message}'
    except requests.ConnectionError:
        return None, 'Could not connect to the server.'
    except requests.Timeout:
        return None, 'Request timed out. Please try again.'
    except requests.RequestException as e:
        return None, f'Error submitting rating: {str(e)}'
