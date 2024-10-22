import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from frontend.utils import load_data, plot_histogram, plot_bar, plot_transition_heatmap


st.set_page_config(layout='centered', initial_sidebar_state='collapsed')

df_dict = load_data()
df = df_dict['origin_df']
df_pop = df[df['genre'] == 'pop']
df_classical = df[df['genre'] == 'classical']
color_map = {'pop': '#1f77b4', 'classical': '#ff7f0e'}


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
fig_npvi_violin = px.violin(df, y='npvi', x='genre', color='genre', box=True, points='all',
                              title='nPVI Distribution by Genre',
                              color_discrete_map=color_map)
fig_npvi_violin.update_layout(legend=dict(x=0.87, y=0.95, bgcolor='rgba(255, 255, 255, 0.5)'))
st.plotly_chart(fig_npvi_violin)


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
                         trendline='ols', trendline_scope='trace',
                         color_discrete_map=color_map)
st.plotly_chart(fig_nd_npvi)

st.write('Are longer songs with more rhythmic variability in classical vs. pop?')
fig_dur_npvi = px.scatter(df, x='duration', y='npvi', color='genre', opacity=0.75,
                          title='nPVI vs Duration by Genre',
                          labels={'duration': 'duration', 'npvi': 'npvi'},
                          trendline='ols', trendline_scope='trace',
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
mean_pcdist1 = df_dict['pitch_class_dist']
for genre in ['pop', 'classical']:
    plot_bar(mean_pcdist1, x_axis='pitch_classes', y_axis=genre,
             title=f'Mean Pitch Class Distribution Probability of {genre.capitalize()} Dataset',
             color=[color_map[genre]], x_label='pitch class')


# """==========================pitch class transition=========================="""
mean_pcdist2 = df_dict['pitch_transition_dist']
plot_transition_heatmap(mean_pcdist2['pop'], 'Blues',
                        'Pitch Transition Heatmap of Pop Dataset', mean_pcdist2['labels'])
plot_transition_heatmap(mean_pcdist2['classical'], 'Oranges',
                        'Pitch Transition Heatmap of Classical Dataset', mean_pcdist2['labels'])


# """==========================intervals=========================="""
mean_ivdist1 = df_dict['interval_dist']

intervals = mean_ivdist1['intervals'].tolist()
tick_labels = [label if i % 3 == 0 else '' for i, label in enumerate(intervals)]

melted_df = mean_ivdist1.melt(id_vars='intervals', var_name='genre', value_name='probability')
plot_bar(melted_df, x_axis='intervals', y_axis='probability', color='genre', color_map=color_map,
         title=f'Mean Interval Distribution Probability by Genre', sort=False, tick_labels=tick_labels)


# """==========================interval size=========================="""
intervals_without_directions = ['P1', 'MI2', 'MA2', 'MI3', 'MA3', 'P4', 'D5', 'P5', 'MI6', 'MA6', 'MI7', 'MA7', 'P8']
mean_ivsizedist1 = df_dict['interval_size_dist']
melted_df = mean_ivsizedist1.melt(id_vars='intervals', var_name='genre', value_name='probability')

plot_bar(melted_df, 'intervals', 'probability', color='genre', color_map=color_map,
         title=f'Mean Interval Size Distribution Probability by Genre', sort=False)


# """==========================interval direction=========================="""
mean_ivdirdist1 = df_dict['interval_dir_dist']
melted_df = mean_ivdirdist1.melt(id_vars='intervals', var_name='genre', value_name='probability')

plot_bar(melted_df, 'intervals', 'probability', color='genre', color_map=color_map,
         title=f'Mean Interval Direction Distribution Probability by Genre', sort=False)


# """==========================interval transition=========================="""
mean_ivdist2 = df_dict['interval_transition_dist']
plot_transition_heatmap(mean_ivdist2['pop'], 'Blues',
                        'Interval Transition Heatmap of Pop Dataset', mean_ivdist2['labels'],
                        tick_labels=tick_labels)
plot_transition_heatmap(mean_ivdist2['classical'], 'Oranges',
                        'Interval Transition Heatmap of Classical Dataset', mean_ivdist2['labels'],
                        tick_labels=tick_labels)


# """==========================complexity & originality & gradus=========================="""
features = ['complexity', 'originality', 'gradus']

fig = make_subplots(rows=1, cols=3)
for i, feature in enumerate(features):
    pop_data = df_pop[feature].dropna()
    classical_data = df_classical[feature].dropna()

    fig.add_trace(
        go.Histogram(x=pop_data, name='Pop', histnorm='probability', marker_color=color_map['pop'], opacity=0.75,
                     showlegend=True if i == 0 else False), row=1, col=i + 1
    )

    fig.add_trace(
        go.Histogram(x=classical_data, name='Classical', histnorm='probability', marker_color=color_map['classical'],
                     opacity=0.75, showlegend=True if i == 0 else False), row=1, col=i + 1
    )

    fig.update_xaxes(title_text=feature, row=1, col=i + 1)

fig.update_layout(title_text='Histograms of Complexity, Originality, and Gradus(Melodiousness) by Genre',
                  barmode='overlay', showlegend=True, legend=dict(x=1, y=1),
                  height=500, width=1000)
st.plotly_chart(fig)

fig_cp_og_gd = px.scatter_3d(df[['complexity', 'originality', 'gradus', 'genre']].dropna(), x='complexity',
                             y='originality', z='gradus', color='genre', color_discrete_map=color_map, size_max=1,
                             opacity=0.75)
st.plotly_chart(fig_cp_og_gd)


