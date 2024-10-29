import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from utils import load_data, plot_histogram, plot_bar, plot_transition_heatmap, classify_key_type, plot_pie, change_container_width


st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
change_container_width(75)

df_dict = load_data()
df = df_dict['origin_df']
df_pop = df[df['genre'] == 'pop']
df_classical = df[df['genre'] == 'classical']
color_map = {'pop': '#1f77b4', 'classical': '#ff7f0e'}

st.title('Musical Characteristics Analysis: Classical vs Pop Music')
st.write("""
Explore the distinctive characteristics and patterns that differentiate classical and pop music 
through data-driven analysis. This analysis covers key distributions, rhythmic patterns, 
pitch characteristics, and compositional complexity.
For the first two analyses, the entire dataset is used, with 909 pop and 1,282 classical samples. 
The latter two analyses focus on a subset of the data, which are compatible with the MIDI toolbox, 
comprising 173 pop and 106 classical samples.
""")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    '🎵 Keys & Tonality', 
    '⏱️ Rhythm & Time',
    '🎼 Pitch & Range',
    '↔️ Pitch Intervals',
    '🔄 Complexity Metrics'
])


with tab1:
    st.header('Keys and Tonality Analysis')
    st.write("""
    ### Key Question: 
    - How do key preferences differ between classical and pop music? 
    - What might these differences tell us about these two genre of music?
    """)
    # key distribution
    col1, col2 = st.columns([1, 1])
    with col1:
        plot_histogram(df_pop, 'key', 'Histogram of Keys in Pop Dataset',
                       category_orders={'key': df_pop['key'].value_counts().index},
                       color_discrete_sequence=[color_map['pop']])
    with col2:
        plot_histogram(df_classical, 'key', 'Histogram of Keys in Classical Dataset',
                       category_orders={'key': df_classical['key'].value_counts().index},
                       color_discrete_sequence=[color_map['classical']])
    # key type pie chart
    col1, col2 = st.columns([1, 1])
    with col1:
        pop_key_type = classify_key_type(df_pop)
        plot_pie(pop_key_type, 'key_type', 'count', title='Pop key types')
    with col2:
        classical_key_type = classify_key_type(df_classical)
        plot_pie(classical_key_type, 'key_type', 'count', title='Classical key types')

    st.write("""
    ### Key Insights:
    - Most Common Keys:
        - Pop music: G major (~7.5%) leads as the most used key, followed by C major (~6.9%), and D major (~6.1%). These 
        three keys together account for about for about 20.5of all pop songs.
        - Classical music: C major stands out as the dominant key (~8.2%), G# major (~5.9%) and C# major (~5.7%) are 
        the next most common.
        - Classical and pop music both showed a strong preference for **C major**
    - Major vs Minor Distribution:
        - Both genres favor major keys, but with different proportions
        - Pop music shows a stronger preference for major keys (22.2% difference), while classical music has a slightly 
        more balanced distribution between major and minor keys (18% difference)
        - Pop's stronger preference for major keys aligns with its generally upbeat, commercial nature
        - Classical's more balanced distribution reflects its broader emotional range and compositional complexity
    - Pop Music:
        - The stronger bias towards major keys indicates a focus on accessible, mood-consistent harmonies
        - The steep decline in key distribution suggests more standardized harmonic choices
    - Classical Music:
        - More even distribution across different keys shows greater harmonic flexibility
        - Higher proportion of minor keys indicates more frequent modulation and emotional contrast
        - The gradual decline in key usage suggests more diverse harmonic exploration
    """)
    with st.expander('📝 Note on Musical Keys and Emotions'):
        st.write("""
        **Musical Keys and Emotional Associations:**

        🎵 **Major Keys**
        - Generally associated with happy, bright, and uplifting emotions
        - Create a sense of resolution and stability

        🎵 **Minor Keys**
        - Typically evoke feelings of sadness, melancholy, or introspection
        - Used to convey more complex or somber emotions
        
        ---
        *Reference: [Our Music World - The Emotional Effects of Musical Keys](https://www.ourmusicworld.com/archives/13867)*
    
        """)


with tab2:
    st.header('Rhythm and Temporal Patterns')
    st.write("""    
    ### Key Questions: 
    1. How does song length vary across different genres?
    2. Which genres show the most rhythmic variability?
    3. Which genres tend to have higher note density?
    4. Is there a correlation between note density and rhythmic variability in these two genres?
    5. Are longer songs with more rhythmic variability?
    """)

    # song duration
    plot_histogram(df, 'duration', 'Histogram of Duration by Genre', color='genre',
                   histnorm='probability', barmode='overlay',
                   color_discrete_map=color_map, opacity=0.75, marginal='box')
    st.write('##### Findings')
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("""
        - Pop 
            - shows a much narrower duration range, primarily clustered between 150-400 seconds 
            (roughly 2.4-6.5 minutes)
            - the distribution has a clear peak around 200-250 seconds (3.3-4.2 minutes) and is normal-like 
            - appears more standardized in length
        """)
    with col2:
        st.write("""
        - Classical
            - has a much wider duration spread, extending well beyond 2000 seconds (>33 minutes)
            - shows a right-skewed distribution with a long tail, indicating many longer pieces
            - the box plot shows more outliers in classical music
            - shows much more variability in duration, suggesting greater compositional freedom        
        """)

    # nPVI
    col1, col2 = st.columns([1, 1])
    with col1:
        # histogram
        plot_histogram(df, 'npvi', 'Histogram of nPVI(normalised Pairwise Variability Index)',
                       color='genre', histnorm='probability', barmode='overlay',
                       color_discrete_map=color_map, opacity=0.75, marginal='box')
    with col2:
        # violin plot
        fig_npvi_violin = px.violin(df, y='npvi', x='genre', color='genre', box=True, points='all',
                                      title='nPVI Distribution by Genre',
                                      color_discrete_map=color_map)
        fig_npvi_violin.update_traces(marker=dict(size=3))
        fig_npvi_violin.update_layout(legend=dict(x=0.87, y=0.95))
        st.plotly_chart(fig_npvi_violin)
    with st.expander('📝 Note on Rhythmic Variability (nPVI)'):
        st.write("""
        The normalized Pairwise Variability Index (nPVI) measures the degree of durational contrast between successive 
        notes. Higher values indicate more variable rhythm patterns.
        This measure is borne out of language research. It has been noted that variability of vowel duration is greater 
        in stress- vs. syllable-timed guages (Grabe & Low, 2002). This measure accounts for the viability of durations 
        and is also called "normalized Pairwise Variability Index" (nPVI). Patel & Daniele have applied it to 
        music (2003) by comparing whether the prosody of different languages is also reflected in music. There is 
        a clear difference between a sample of works by French and English composers.
        
        ---
        *References:*
        
        Eerola, T., & Toiviainen, P. (2004). MIDI toolbox: MATLAB tools for music research.
        
        Patel, A. D. & Daniele, J. R. (2003). An empirical comparison of rhythm in language and music. 
        Cognition, 87, B35-B45.
        
        Grabe, E., & Low, E. L. (2002). Durational variability in speech and the rhythm class hypothesis. 
        In C. Gussen-hoven & N. Warner, Laboratory phonology (pp. 515-546). 7. Berlin: Mouton de Gruyter.
        """)
    st.write("""
    ##### Findings
    - Both genres show approximately normal distributions, and the range of nPVI values is roughly between 30-80 for 
    both genres, with some outliers
    - Classical music shows a slightly higher median nPVI value (around 55-60)
    - The box plots indicate that the interquartile ranges (middle 50% of data) overlap considerably between genres
    - Classical music demonstrates somewhat greater variability in nPVI values, shown by the wider spread in both the 
    histogram and violin plot
    """)

    col1, col2 = st.columns([6, 4])
    with col1:
        # note density
        plot_histogram(df, 'note_density', 'Note Count per Beat by Genre', color='genre',
                       histnorm='probability', barmode='overlay',
                       color_discrete_map=color_map, opacity=0.75,
                       xaxis_title='note density (notes per beat)', marginal='box')
    with col2:
        fig_nd_npvi = px.scatter(df, x='note_density', y='npvi', color='genre', opacity=0.75,
                                 title='nPVI vs Note Density by Genre',
                                 labels={'npvi': 'nPVI', 'note_density': 'note density'},
                                 trendline='ols', trendline_scope='trace',
                                 color_discrete_map=color_map)
        fig_nd_npvi.update_traces(marker=dict(size=3))
        fig_nd_npvi.update_layout(legend=dict(x=0.75, y=0.95))
        st.plotly_chart(fig_nd_npvi)
    st.write("""
    ##### Findings
    - Notes per beat typically fall between 2-10, with most concentrated between 4-7
    - Both genres show a negative correlation between note density and nPVI，as note density increases, rhythmic 
    variability (nPVI) tends to decrease, while classical shows a steeper negative slope, suggesting stronger correlation.
    - Higher note densities generally correspond to more regular rhythmic patterns (lower nPVI), this might reflect 
    practical limitations in performing complex rhythms at high note densities
    - Classical music shows greater variability in both measures, while pop music tends to cluster more tightly around 
    certain values
    """)

    col1, col2 = st.columns([6, 4])
    with col1:
        fig_dur_npvi = px.scatter(df, x='duration', y='npvi', color='genre', opacity=0.4,
                                  title='nPVI vs Duration by Genre',
                                  labels={'duration': 'duration', 'npvi': 'npvi'},
                                  trendline='ols', trendline_scope='trace',
                                  color_discrete_map=color_map)
        fig_dur_npvi.update_layout(legend=dict(x=0.79, y=0.95))
        st.plotly_chart(fig_dur_npvi)
    with col2:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write("""
        ##### Findings
        - Density of points is highest in the 200-400 second range
        - Length of a classical piece doesn't strongly has positive correlation to its rhythmic complexity, while pop 
        music shows increasing trend when it get longer.
        - Classical shows greater range in both dimensions
        """)


with tab3:
    st.header('Pitch Characteristics and Range')
    st.write("""
    ### Key Questions:
    1. How do the pitch preferences differ between Classical and Pop music?
    2. What are the characteristic pitch patterns in each genre?
    3. How do the different patterns of pitch transitions between Classical and Pop music reflect changes in 
    compositional approaches?
    """)
    # pitch range
    col1, col2 = st.columns([6, 4])
    with col1:
        plot_histogram(df, 'pitch_range', 'Pitch range in semitones by genre', color='genre', opacity=0.75,
                       histnorm='probability', barmode='overlay', color_discrete_map=color_map,
                       xaxis_title='pitch range in semitones', marginal='box')
    with col2:
        st.write('')
        st.write('')
        st.write("""
        ##### Findings
        - Classical music shows a bimodal distribution with main peak around 75-80 semitones, while pop music has a 
        single, concentrated peak around 50-60 semitones
        - Classical music generally exploits a broader range of pitches, likely due to:
            - Use of full orchestral range
            - More dramatic dynamic contrasts
        - Pop music's narrower range likely reflects:
            - Focus on vocal-friendly ranges
            - Modern production conventions  
        """)

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

    # pitch class
    mean_pcdist1 = df_dict['pitch_class_dist']
    col1, col2 = st.columns([1, 1])
    with col1:
        plot_bar(mean_pcdist1, x_axis='pitch_classes', y_axis='pop',
                 title='Mean Pitch Class Distribution Probability of Pop Dataset',
                 color=[color_map['pop']], x_label='pitch class')
    with col2:
        plot_bar(mean_pcdist1, x_axis='pitch_classes', y_axis='classical',
                 title='Mean Pitch Class Distribution Probability of Classical Dataset',
                 color=[color_map['classical']], x_label='pitch class')
    st.write("""
    ##### Findings
    - Both genres show a relatively even distribution of pitch classes, with probabilities ranging roughly between 
    0.06-0.09
    - No pitch class is dramatically over- or under-represented in either genre
    - Classical's more gradual probability decline suggests that it uses more extensive modulation practices and has 
    broader exploration of key relationships
    """)

    # pitch class transition
    mean_pcdist2 = df_dict['pitch_transition_dist']
    col1, col2 = st.columns([1, 1])
    with col1:
        plot_transition_heatmap(mean_pcdist2['pop'], 'Blues',
                                'Pitch Transition Heatmap of Pop Dataset', mean_pcdist2['labels'])
    with col2:
        plot_transition_heatmap(mean_pcdist2['classical'], 'Oranges',
                                'Pitch Transition Heatmap of Classical Dataset', mean_pcdist2['labels'])
    st.write("""
    ##### Findings
    - Classical music has stronger probabilities (up to 0.04) compared to Pop (up to 0.02), and classical music shows more 
    concentrated transition patterns, while pop music displays more diffused transitions.
    - Classical music shows strong diagonal-adjacent patterns, indicating stepwise motion (moving to neighboring pitches)
    - Pop music's more evenly distributed transitions suggest a more varied chord progressions and less strict adherence
     to traditional music composition rules. 
    """)


with tab4:
    st.header('Interval Analysis')
    st.write("""
    ### Key Questions:
    1. What interval patterns characterize each genre?
    2. How do interval sizes and directions differ between genres?
    3. What do transition patterns reveal about melodic construction?
    """)
    # intervals
    mean_ivdist1 = df_dict['interval_dist']

    intervals = mean_ivdist1['intervals'].tolist()
    tick_labels = [label if i % 3 == 0 else '' for i, label in enumerate(intervals)]

    melted_df = mean_ivdist1.melt(id_vars='intervals', var_name='genre', value_name='probability')
    plot_bar(melted_df, x_axis='intervals', y_axis='probability', color='genre', color_map=color_map,
             title=f'Mean Interval Distribution Probability by Genre', sort=False)
    st.write("""
    ##### Findings
    - Pop music shows two more pronounced peaks at ascending and descending major seconds (±M2), while classical music 
    has a more normal-like distribution
    - Pop music has a lower usage of extreme intervals (±P8, ±M6) compare to classical music
    - Pop music heavily concentrated in ±P5 range, showing strong preferences for specific intervals, which suggests 
    simpler melodic patterns 
    - Classical music regularly uses full octave range, demonstrating more diverse interval choices, which indicates 
    more complex melodic writing
    - Strongest presence of major seconds (±M2) > 0.15 probability and low in perfect unison(P1) in Pop music suggests 
    that pop melodies favor step-wise motion more than staying on the same note.
    - Two pitch interval plots are coherent with the pitch class transition heatmaps. 
    """)

    col1, col2 = st.columns([1, 1])
    with col1:
        # interval size
        intervals_without_directions = ['P1', 'MI2', 'MA2', 'MI3', 'MA3', 'P4', 'D5', 'P5', 'MI6', 'MA6', 'MI7', 'MA7', 'P8']
        mean_ivsizedist1 = df_dict['interval_size_dist']
        melted_df = mean_ivsizedist1.melt(id_vars='intervals', var_name='genre', value_name='probability')

        plot_bar(melted_df, 'intervals', 'probability', color='genre', color_map=color_map,
                 title=f'Mean Interval Size Distribution Probability by Genre', sort=False)
    with col2:
        # interval direction
        mean_ivdirdist1 = df_dict['interval_dir_dist']
        melted_df = mean_ivdirdist1.melt(id_vars='intervals', var_name='genre', value_name='probability')

        plot_bar(melted_df, 'intervals', 'probability', color='genre', color_map=color_map,
                 title=f'Mean Interval Direction Distribution Probability by Genre', sort=False)
    st.write("""
    ##### Findings
    - Both genres show decreasing probabilities as interval size increases after major seconds.
    - Diminished Fifth (D5) is notably lower than surrounding intervals for both genres, because it is historically 
    known as a dissonant interval.
    - Except for the peak location difference (MA2 for pop and MI2 for classical), both genres follow very similar 
    relative patterns, this suggests fundamental similarities in melodic construction between the genres
    - Strong negative values for MI2/MA2 and MI3/MA3 in the right graph indicate preference for descending motion
    - Notable differences in MA6 and MA7 where classical and pop show opposite directional preferences
    """)

    # interval transition
    mean_ivdist2 = df_dict['interval_transition_dist']
    col1, col2 = st.columns([1, 1])
    with col1:
        plot_transition_heatmap(mean_ivdist2['pop'], 'Blues',
                                'Interval Transition Heatmap of Pop Dataset', mean_ivdist2['labels'],
                                tick_labels=tick_labels)
    with col2:
        plot_transition_heatmap(mean_ivdist2['classical'], 'Oranges',
                                'Interval Transition Heatmap of Classical Dataset', mean_ivdist2['labels'],
                                tick_labels=tick_labels)
    st.write("""
    ##### Findings
    - Classical shows higher maximum transition probabilities (0.07 vs 0.04)
    - Pop has more sharp contrasts between common and uncommon transitions, while classical transitions appear more 
    gradual in probability changes
    - Pop music shows the strongest transitions appear near the center (around ±m2, P1) and notable concentration 
     of activity in the central region. The frequent transitions between -m2 (descending minor second) to +m2 
     (ascending minor second) or vice versa indicates a "wavering" melodic contour. For example: 
     
        ```
        Note sequence: C -> B -> C# -> B -> C
         
        Intervals:        -m2   +m2   -m2   +m2
        ```
    """)


with tab5:
    st.header('Musical Complexity Analysis')
    st.write("""
    ### Key Questions:
    1. How do objective measures of complexity differ between genres?
    2. What is the relationship between complexity, originality, and melodiousness?
    """)
    # complexity & originality & gradus
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
    fig.update_yaxes(title_text="probability", row=1, col=1)
    fig.update_layout(title_text='Histograms of Complexity, Originality, and Gradus(Melodiousness) by Genre',
                      barmode='overlay', showlegend=True, legend=dict(x=1, y=1),
                      height=500, width=1000)
    st.plotly_chart(fig)
    with st.expander('📝 Note on complexity, originality and gradus'):
        st.write("""
        - **Complexity**
        
            Expectancy-based model of melodic complexity based either on pitch or rhythm-related components or 
            on an optimal combination of them together. The higher the output value is, the more complex the music 
            piece is.
        - **Originality**
        
            Calculates Simonton's melodic originality score (1984) based on 2nd order pitch-class distribution of 
            classical music that are derived from 15618 classical music themes. The score is scaled between 0 and 10, 
            higher value indicates higher melodic originality.
        - **Gradus(Melodiousness)**
        
            Calculates the degree of melodiousness (gradus suavitatis), proposed by L. Euler (1707-1783). He suggested
            that the "degree of melodiousness depends on calculations made by the mind: fewer calculations, the more 
            pleasant the experience. This method is implemented by a numerical technique based on the decomposition
            of natural numbers into a product of powers of different primes." Lower value indicates high melodiousness.
            (Leman, 1995, p. 5)

        ---
        *References:*
        
        Eerola, T., & Toiviainen, P. (2004). MIDI toolbox: MATLAB tools for music research.

        Eerola, T. (in press). Expectancy-violation and information-theoretic models of melodic complexity. Empirical 
        Musicology Review.

        Eerola, T. & North, A. C. (2000) Expectancy-Based Model of Melodic Complexity. 
        In Woods, C., Luck, G.B., Brochard, R., O'Neill, S. A., and Sloboda, J. A. (Eds.) Proceedings of the Sixth 
        International Conference on Music Perception and Cognition. Keele, Staffordshire, UK: Department of Psychology.

        Eerola, T., Himberg, T., Toiviainen, P., & Louhivuori, J. (2006). Perceived complexity of Western and African 
        folk melodies by Western and African listeners. Psychology of Music, 34(3), 341-375.
        
        Simonton, D. K. (1984). Melodic structure and note transition probabilities: A content analysis of 15,618 
        classical themes. Psychology of Music, 12, 3-16. 
        
        Simonton, D. K. (1994). Computer content analysis of melodic structure: Classical composers and their 
        compositions. Psychology of Music, 22, 31-43.
        
        Euler, L. (1739). Tentamen novae theoriae musicae. Leman, M.  (1995). Music and schema theory: Cognitive 
        foundations of systematic musicology. Berlin: Springer.
        """)

    fig_cp_og_gd = px.scatter_3d(df[['complexity', 'originality', 'gradus', 'genre']].dropna(), x='complexity',
                                 y='originality', z='gradus', color='genre', color_discrete_map=color_map, size_max=1,
                                 opacity=0.75)
    st.plotly_chart(fig_cp_og_gd)
    st.write("""
    ##### Findings
    - Complexity:
        - Pop music tends to cluster around a lower complexity score (centered around 5-6), classical music shows hight 
        complexity overall, and two distribution have minimal overlap, suggesting a clear distinction in complexity between 
        the genres. In the 3D scatter plot, this distinction on the complexity axis can be clearly observed.
    - Originality:
        - Both genres show some right skew in the originality distribution, classical music has a higher score overall 
        and the cluster is concentrated around 7-9, while pop music has a more scattered originality score ranging from 
        5-9.
    - Gradus:
        - Two genres show a significant overlap. Classical music has a bimodal distribution with peaks around scores 6 
        and 8.
    - Overall:
        - Classical music consistently demonstrates higher complexity and originality than pop music
        - Classical music cluster tends to cluster more tightly in the scatter plot and fewer outliers, might due to 
        fewer sample count. 
        - According to Euler's principle, lower scores indicate higher melodiousness (fewer mental calculations 
        needed). In the distribution of gradus, classical music shows higher probability of higher
        gradus score. This makes sense because pop music is often created to be immediately catchy and easily 
        processed by listeners, requiring fewer "mental calculations". In contrast, classical music frequently uses 
        complex harmonic structures, modulations, and intricate melodic patterns that require more mental processing.
    """)

