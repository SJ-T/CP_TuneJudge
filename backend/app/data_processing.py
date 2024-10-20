import numpy as np
import pandas as pd

from .models import Music

pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
intervals = [
    '-P8', '-M7', '-m7', '-M6', '-m6', '-P5', '-d5', '-P4',
    '-M3', '-m3', '-M2', '-m2', 'P1', '+m2', '+M2', '+m3',
    '+M3', '+P4', '+d5', '+P5', '+m6', '+M6', '+m7', '+M7', '+P8'
]
intervals_without_directions = ['P1', 'MI2', 'MA2', 'MI3', 'MA3', 'P4', 'D5', 'P5', 'MI6', 'MA6', 'MI7', 'MA7', 'P8']


def get_processed_music_data():
    music_data = Music.objects.filter(label__in=['pop', 'classical']).values()
    df = pd.DataFrame(music_data)
    df['genre'] = df['label']
    data = df.to_dict(orient='records')
    for item in data:
        for key, value in item.items():
            if isinstance(value, (np.int64, np.float64)):
                item[key] = float(value)
            elif isinstance(value, np.ndarray):
                item[key] = value.tolist()
    processed_data = {
        'origin_df': data,
        'pitch_class_dist': get_pitch_class_distribution(df),
        'pitch_transition_dist': get_pitch_transition_distribution(df),
        'interval_dist': get_interval_distribution(df),
        'interval_size_dist': get_interval_size_distribution(df),
        'interval_dir_dist': get_interval_dir_distribution(df),
        'interval_transition_dist': get_interval_transition_distribution(df),
    }

    return processed_data


def get_pitch_class_distribution(df):
    return {
        'pop': df[df['genre'] == 'pop']['pc_dist1'].apply(pd.Series).mean().tolist(),
        'classical': df[df['genre'] == 'classical']['pc_dist1'].apply(pd.Series).mean().tolist(),
        'pitch_classes': pitch_classes
    }


def get_pitch_transition_distribution(df):
    result = {}
    for genre in ['pop', 'classical']:
        sampled_data = df[df['genre'] == genre]['pc_dist2'].dropna()
        mean_df = pd.DataFrame(np.mean(np.stack(sampled_data), axis=0), index=pitch_classes, columns=pitch_classes)
        result[genre] = mean_df.to_dict(orient='split')
    result['labels'] = pitch_classes
    return result


def get_interval_distribution(df):
    return {
        'pop': df[df['genre'] == 'pop']['iv_dist1'].apply(pd.Series).mean().tolist(),
        'classical': df[df['genre'] == 'classical']['iv_dist1'].apply(pd.Series).mean().tolist(),
        'intervals': intervals
    }


def get_interval_size_distribution(df):
    return {
        'pop': df[df['genre'] == 'pop']['ivsize_dist1'].apply(pd.Series).mean().tolist(),
        'classical': df[df['genre'] == 'classical']['ivsize_dist1'].apply(pd.Series).mean().tolist(),
        'intervals': intervals_without_directions
    }


def get_interval_dir_distribution(df):
    return {
        'pop': df[df['genre'] == 'pop']['ivdir_dist1'].apply(pd.Series).mean().tolist(),
        'classical': df[df['genre'] == 'classical']['ivdir_dist1'].apply(pd.Series).mean().tolist(),
        'intervals': intervals_without_directions[1:]
    }


def get_interval_transition_distribution(df):
    result = {}
    for genre in ['pop', 'classical']:
        sampled_data = df[df['genre'] == genre]['iv_dist2'].dropna()
        mean_df = pd.DataFrame(np.mean(np.stack(sampled_data), axis=0), index=intervals, columns=intervals)
        result[genre] = mean_df.to_dict(orient='split')
    result['labels'] = intervals
    return result
