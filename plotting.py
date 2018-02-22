import pandas as pd


def make_df_from_cluster_list(clusters):
    frames = []
    cols = ['heatmister_id', 'distance', 'speed', 'location', 'osha']

    for i, cluster in enumerate(clusters):
        df = pd.DataFrame(cluster, columns=cols)
        df['cluster'] = i
        frames.append(df)

    df = pd.concat(frames, ignore_index=True)
    df['distance'] = df['distance'].astype('float')
    df['speed'] = df['speed'].astype(int)

    return df


class ClusterPlotter():
    def __init__(self):
        self.clusters = []

    def add_cluster_list(self, clusters):
        self.clusters.append(make_df_from_cluster_list(clusters))