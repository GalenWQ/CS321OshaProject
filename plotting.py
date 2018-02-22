import pandas as pd
import seaborn as sns
sns.set_style("whitegrid")


# Decision Tree

def make_plot(data, cols):
    melted_data = data.melt(
        id_vars='fold',
        value_vars=cols)

    g = sns.factorplot(
        x="fold", y="value", kind='point',
        hue='variable', data=melted_data, size=10,
        saturation=.5)
    return g


class ClusterPlotter:
    """For plotting k-means clustering!"""

    def __init__(self):
        self.folds = []

    def add_cluster_list(self, clusters):
        """Given a list of clusters, makes as DF and adds to self.folds"""
        self.folds.append(self.make_df_from_cluster_list(clusters))

    def make_plot(self):
        """Uses data in self.folds to create plots for all 10 folds"""
        data = self.combine_fold_frames(self.folds)
        p = sns.lmplot(
            x='distance', y='speed', data=data,
            fit_reg=False, hue='cluster', col='fold', col_wrap=5)
        return p

    @staticmethod
    def make_df_from_cluster_list(clusters):
        """Returns pandas dataframe repr of list of lists containing
        HeatMiser data in each cluster"""
        cols = ['heatmister_id', 'distance', 'speed', 'location', 'osha']
        frames = []
        for i, cluster in enumerate(clusters):
            df = pd.DataFrame(cluster, columns=cols)
            df['cluster'] = i
            frames.append(df)
        df = pd.concat(frames, ignore_index=True)
        df['distance'] = df['distance'].astype('float')
        df['speed'] = df['speed'].astype(int)
        return df

    @staticmethod
    def combine_fold_frames(folds):
        """Used to combine the df for each fold
        into long, 'tidy' format"""
        dfs = []
        for i, fold_df in enumerate(folds):
            fold_df['fold'] = i + 1
            dfs.append(fold_df)
        return pd.concat(dfs)
