import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

from config import API_BASE_URL


def load_css(file_path='static/style.css'):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


"""data analysis"""
@st.cache_data
def load_data():
    response = requests.get(f'{API_BASE_URL}feature-analysis/')
    data = response.json()
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
    return df_dict


def plot_histogram(data, x_col, title, xaxis_title=None, color=None, **kwargs):
    fig = px.histogram(data, x=x_col, title=title, color=color, **kwargs)
    if xaxis_title:
        fig.update_layout(xaxis_title=xaxis_title)
    fig.update_layout(legend=dict(x=0.87, y=0.95, bgcolor='rgba(255, 255, 255, 0.5)'))
    st.plotly_chart(fig)


def plot_bar(df, x_axis, y_axis, title, color, **kwargs):
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


def plot_transition_heatmap(df, color_scale, title, labels, **kwargs):
    tick_labels = kwargs.get('tick_labels', None)

    matrix_data = np.array([row for row in df['data']])
    fig = go.Figure(data=go.Heatmap(
        z=matrix_data,
        x=df['columns'],
        y=df['index'],
        colorscale=color_scale))
    fig.update_layout(
        title=title,
    )
    if tick_labels:
        fig.update_xaxes(tickvals=list(range(len(tick_labels))), ticktext=list(tick_labels))
        fig.update_yaxes(tickvals=list(range(len(tick_labels))), ticktext=list(tick_labels)[::-1])
    st.plotly_chart(fig)


"""turing test"""
def fetch_random_music():
    response = requests.get(f'{API_BASE_URL}music/random/')
    response.raise_for_status()
    return response.json()


def submit_rating(song_id, rating):
    response = requests.post(f'{API_BASE_URL}ratings/rate_song/', json={'song': song_id, 'rating': rating})
    response.raise_for_status()
    return response.json()
