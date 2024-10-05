import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv('frontend/features_data/midi_ds_features.csv')
df_pop = df[df['genre'] == 'pop']
df_classical = df[df['genre'] == 'classical']
color_map = {'pop': '#1f77b4', 'classical': '#ff7f0e'}
seed = 42
num_samples = 106


def restore_matrix_from_str(matrix_str):
    if pd.isna(matrix_str):
        return matrix_str
    else:
        rows = matrix_str.strip('[]').split(';')
        matrix = np.array([list(map(float, row.split())) for row in rows])
        return matrix


def get_mean_iv_df_1D(intervals, feature):
    np.random.seed(seed)
    mean_dist = pd.DataFrame({
        'intervals': intervals,
        'pop': df[df['genre'] == 'pop'][feature].dropna().sample(n=num_samples, random_state=seed)
        .apply(lambda x: np.fromstring(x.strip('[]'), sep=' ')).mean(),
        'classical': df[df['genre'] == 'classical'][feature].dropna().
        apply(lambda x: np.fromstring(x.strip('[]'), sep=' ')).mean()
    })
    melted_df = mean_dist.melt(id_vars='intervals', value_vars=['pop', 'classical'], var_name='genre',
                               value_name='probability')

    return melted_df


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
    if sort:
        fig = px.bar(df, x=x_axis, y=y_axis, color_discrete_sequence=color, title=title,
                     labels={genre: 'probability', x_axis: x_label},
                     category_orders={x_axis: df.sort_values(genre, ascending=False)[x_axis]})
    else:
        fig = px.bar(df, x=x_axis, y=y_axis, color=color, title=title, barmode='group',
                     labels={genre: 'probability', x_axis: x_label}, color_discrete_map
                     =kwargs.get('color_map', None))
    if tick_labels:
        fig.update_xaxes(tickvals=list(range(len(tick_labels))), ticktext=list(tick_labels))
    st.plotly_chart(fig)

def plot_transition_heatmap(genre, feature, color_scale, title, labels, **kwargs):
    tick_labels = kwargs.get('tick_labels', None)
    np.random.seed(seed)
    sampled_data = df[df['genre'] == genre][feature].dropna().sample(n=num_samples, random_state=seed).values
    mean_df = pd.DataFrame(np.mean(np.stack(sampled_data), axis=0), index=labels, columns=labels)
    mean_df = mean_df.iloc[::-1]
    fig = px.imshow(mean_df, x=labels, y=labels[::-1], title=title,
                    color_continuous_scale=color_scale)
    if tick_labels:
        fig.update_xaxes(tickvals=list(range(len(tick_labels))), ticktext=list(tick_labels))
        fig.update_yaxes(tickvals=list(range(len(tick_labels))), ticktext=list(tick_labels)[::-1])
    st.plotly_chart(fig)


# """==========================keys=========================="""
plot_histogram(df_pop, 'key', 'Histogram of Keys in Pop Dataset',
               category_orders={'key': df_pop['key'].value_counts().index},
               color_discrete_sequence=[color_map['pop']])

plot_histogram(df_classical, 'key', 'Histogram of Keys in Classical Dataset',
               category_orders={'key': df_classical['key'].value_counts().index},
               color_discrete_sequence=[color_map['classical']])

plot_histogram(df, 'key', 'Histogram of Keys by Genre', color='genre', histnorm='probability',
               barmode='group', color_discrete_map=color_map,
               category_orders={'key': df['key'].value_counts().index})

# """==========================durations=========================="""
plot_histogram(df, 'duration', 'Histogram of Duration by Genre', color='genre',
               histnorm='probability', barmode='overlay',
               color_discrete_map=color_map, opacity=0.75, marginal='box')

# """==========================note durational variability=========================="""
# Histogram
plot_histogram(df, 'npvi', 'Histogram of nPVI(normalised Pairwise Variability Index) by Genre',
               color='genre', histnorm='probability', barmode='overlay',
               color_discrete_map=color_map, opacity=0.75, marginal='box')

# Violin plot
fig_npvi_violin = px.violin(df, y='npvi', x='genre', color='genre', box=True, points="all",
                              title='nPVI Distribution by Genre',
                              color_discrete_map=color_map)
fig_npvi_violin.update_layout(legend=dict(x=0.87, y=0.95, bgcolor='rgba(255, 255, 255, 0.5)'))
st.plotly_chart(fig_npvi_violin)

# fig_key_npvi = go.Figure()
# fig_key_npvi.add_trace(go.Violin(x=df['key'][df['genre'] == 'pop'], y=df['npvi'][df['genre'] == 'pop'],
#                                  legendgroup='pop', scalegroup='pop', name='pop', side='negative', line_color=color_map['pop']
#                                  ))
# fig_key_npvi.add_trace(go.Violin(x=df['key'][df['genre'] == 'classical'], y=df['npvi'][df['genre'] == 'classical'],
#                                  legendgroup='classical', scalegroup='classical', name='classical', side='positive',
#                                  line_color=color_map['classical']
#                                  ))
# fig_key_npvi.update_layout(legend=dict(x=0.87, y=0.95, bgcolor='rgba(255, 255, 255, 0.5)'))
# st.plotly_chart(fig_key_npvi)

# """==========================note density=========================="""
# Histogram
plot_histogram(df, 'note_density', 'Note Count per Beat by Genre', color='genre',
               histnorm='probability', barmode='overlay',
               color_discrete_map=color_map, opacity=0.75,
               xaxis_title='note density (notes per beat)', marginal='box')

st.write('Are higher densities associated with more rhythmic variability in classical vs. pop?')
fig_nd_npvi = px.scatter(df, x='note_density', y='npvi', color='genre', opacity=0.75,
                         title='nPVI vs Note Density by Genre',
                         labels={'npvi': 'nPVI', 'note_density': 'note density'},
                         trendline="ols", trendline_scope="trace",
                         color_discrete_map=color_map)
st.plotly_chart(fig_nd_npvi)

st.write('Are longer songs with more rhythmic variability in classical vs. pop?')
fig_dur_npvi = px.scatter(df, x='duration', y='npvi', color='genre', opacity=0.75,
                          title='nPVI vs Duration by Genre',
                          labels={'duration': 'duration', 'npvi': 'npvi'},
                          trendline="ols", trendline_scope="trace",
                          color_discrete_map=color_map)
st.plotly_chart(fig_dur_npvi)

# """==========================pitch range=========================="""
plot_histogram(df, 'pitch_range', 'Pitch range in semitones by genre', color='genre', opacity=0.75,
               histnorm='probability', barmode='overlay', color_discrete_map=color_map,
               xaxis_title='pitch range in semitones', marginal='box')

st.write('Do longer songs have wider pitch range in classical vs. pop?')
min_density, max_density = st.slider(
    'Select a range of note density (notes per beat)',
    min_value=0.0,
    max_value=15.0,
    value=(0.0, 15.0),
    step=1.0
)
filtered_df = df[(df['note_density'] >= min_density) & (df['note_density'] <= max_density)]
fig_pr_dur_nd = px.scatter(filtered_df, x='pitch_range', y='duration', size='note_density', color='genre',
                           title='Pitch Range vs Duration by Genre with Note Density',
                           labels={'pitch_range': 'pitch range', 'duration': 'duration (s)',
                                   'note_density': 'note density'},
                           color_discrete_map=color_map)
st.plotly_chart(fig_pr_dur_nd)


# """==========================pitch class=========================="""
pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
df['pc_dist1'] = df['pc_dist1'].apply(lambda x: np.fromstring(x.strip('[]'), sep=' '))
mean_pcdist1 = pd.DataFrame({
    'pitch_class': pitch_classes,
    'pop': df[df['genre'] == 'pop']['pc_dist1'].mean(),
    'classical': df[df['genre'] == 'classical']['pc_dist1'].mean()
})
for genre in ['pop', 'classical']:
    plot_bar(mean_pcdist1, 'pitch_class', genre,
             f'Mean Pitch Class Distribution Probability of {genre.capitalize()} Dataset',
             [color_map[genre]], x_label='pitch class')

# """==========================pitch class transition=========================="""
df['pc_dist2'] = df['pc_dist2'].apply(restore_matrix_from_str)

plot_transition_heatmap('pop', 'pc_dist2', 'Blues',
                        'Pitch Transition Heatmap of Pop Dataset', pitch_classes)
plot_transition_heatmap('classical', 'pc_dist2', 'Oranges',
                        'Pitch Transition Heatmap of Classical Dataset', pitch_classes)

# """==========================intervals=========================="""
intervals = [
    '-P8', '-M7', '-m7', '-M6', '-m6', '-P5', '-d5', '-P4',
    '-M3', '-m3', '-M2', '-m2', 'P1', '+m2', '+M2', '+m3',
    '+M3', '+P4', '+d5', '+P5', '+m6', '+M6', '+m7', '+M7', '+P8'
]
tick_labels = [label if i % 3 == 0 else '' for i, label in enumerate(intervals)]

mean_ivdist1 = get_mean_iv_df_1D(intervals, 'iv_dist1')

plot_bar(mean_ivdist1, 'intervals', 'probability', color='genre', color_map=color_map,
         title=f'Mean Interval Distribution Probability by Genre', sort=False, tick_labels=tick_labels)

# """==========================interval size=========================="""
intervals_without_directions = ['P1', 'MI2', 'MA2', 'MI3', 'MA3', 'P4', 'D5', 'P5', 'MI6', 'MA6', 'MI7', 'MA7', 'P8']
mean_ivsizedist1 = get_mean_iv_df_1D(intervals_without_directions, 'ivsize_dist1')

plot_bar(mean_ivsizedist1, 'intervals', 'probability', color='genre', color_map=color_map,
         title=f'Mean Interval Size Distribution Probability by Genre', sort=False)

# """==========================interval direction=========================="""
mean_ivdirdist1 = get_mean_iv_df_1D(intervals_without_directions[1:], 'ivdir_dist1')
plot_bar(mean_ivdirdist1, 'intervals', 'probability', color='genre', color_map=color_map,
         title=f'Mean Interval Direction Distribution Probability by Genre', sort=False)

# """==========================interval transition=========================="""
df['iv_dist2'] = df['iv_dist2'].apply(restore_matrix_from_str)
plot_transition_heatmap('pop', 'iv_dist2', 'Blues',
                        'Interval Transition Heatmap of Pop Dataset', intervals, tick_labels=tick_labels)
plot_transition_heatmap('classical', 'iv_dist2', 'Oranges',
                        'Interval Transition Heatmap of Classical Dataset', intervals, tick_labels=tick_labels)

# """==========================complexity & originality & gradus=========================="""
features = ['complexity', 'originality', 'gradus']

# Create a subplot with 1 row and 3 columns
fig = make_subplots(rows=1, cols=3)

# Loop through each feature to create histograms for both genres
for i, feature in enumerate(features):
    # Remove NaN values for each genre
    pop_data = df_pop[feature].dropna()
    classical_data = df_classical[feature].dropna()

    # Add Pop histogram
    fig.add_trace(
        go.Histogram(x=pop_data, name='Pop', histnorm='probability', marker_color=color_map['pop'], opacity=0.75,
                     showlegend=True if i == 0 else False), row=1, col=i + 1
    )

    # Add Classical histogram
    fig.add_trace(
        go.Histogram(x=classical_data, name='Classical', histnorm='probability', marker_color=color_map['classical'],
                     opacity=0.75, showlegend=True if i == 0 else False), row=1, col=i + 1
    )

    # Update layout for the subplots
    fig.update_xaxes(title_text=feature, row=1, col=i + 1)

# Update layout for the entire figure
fig.update_layout(title_text="Histograms of Complexity, Originality, and Gradus(Melodiousness) by Genre",
                  barmode='overlay', showlegend=True, legend=dict(x=1, y=1),
                  height=500, width=1000)
st.plotly_chart(fig)

fig_cp_og_gd = px.scatter_3d(df[['complexity', 'originality', 'gradus', 'genre']].dropna(), x='complexity',
                             y='originality', z='gradus', color='genre', color_discrete_map=color_map, size_max=1,
                             opacity=0.75)
st.plotly_chart(fig_cp_og_gd)


