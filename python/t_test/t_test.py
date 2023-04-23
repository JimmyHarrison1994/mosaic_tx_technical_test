import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

from scipy.stats import ttest_ind

class TTest:
    
    def __init__(
            self,
            mutations_path,
            gene_ko_path,
            out_path,
            plot=False):
        self.mutations_path = mutations_path
        self.gene_ko_path = gene_ko_path
        self.out_path = out_path
        self.plot = plot

    def _read_data(self):
        mutations_df = pd.read_csv(self.mutations_path, sep='\t')
        mutations_df = mutations_df.set_index('Mutation').transpose().reset_index(names=['Model'])

        gene_ko_df = pd.read_csv(self.gene_ko_path, sep='\t')

        return gene_ko_df.merge(mutations_df, 'inner', on='Model')

    def _assign_columns(self, columns):
        mutations_cols = [x for x in columns if 'mut' in x]
        gene_ko_cols = [x for x in columns if 'KO' in x]

        return mutations_cols, gene_ko_cols

    def _t_test(self, merged_df, mutation, gene_ko):
        return ttest_ind(*merged_df.groupby(mutation)[gene_ko].apply(lambda x:x.values))

    def _populate_row(self, merged_df, mutation, gene_ko):
        row_dict = {}
        row_dict['mutation'] = mutation
        row_dict['gene_ko'] = gene_ko
        row_dict['t_statistic'], row_dict['p_value'] = self._t_test(merged_df, mutation, gene_ko)
        return row_dict

    def plot_t_statistic_heatmap(self, result_df):
        t_statistic_df = result_df.pivot(index='mutation', columns = 'gene_ko', values='t_statistic')
        fig, ax = plt.subplots(1,1)
        sns.heatmap(t_statistic_df, cmap='vlag', center=0, ax = ax, cbar_kws={'label': 't_statistic'})
        ax.set_ylabel('Mutation')
        ax.set_xlabel('Gene KO')
        fig.tight_layout()
        fig.savefig('../results/t_statistic_heatmap.png')

    def plot_minus_log_p_heatmap(self, result_df):
        minus_log_p_df = result_df.pivot(index='mutation', columns = 'gene_ko', values='p_value').applymap(np.log10) * -1
        fig, ax = plt.subplots(1,1)
        sns.heatmap(minus_log_p_df, cmap='vlag', center=0, ax = ax, cbar_kws={'label': r"$-\mathrm{log}_{10}P$"})
        ax.set_ylabel('Mutation')
        ax.set_xlabel('Gene KO')
        fig.tight_layout()
        fig.savefig('../results/p_value_heatmap.png')


    def main(self):
        merged_df = self._read_data()
        mutations_cols, gene_ko_cols = self._assign_columns(merged_df.columns)

        row_list = []
        for mutation in mutations_cols:
            for gene_ko in gene_ko_cols:
                row_list.append(self._populate_row(merged_df, mutation, gene_ko))

        result_df = pd.DataFrame(row_list)
        result_df.to_csv(os.path.join('../results', self.out_path), sep='\t', index=False)

        if self.plot:
            self.plot_t_statistic_heatmap(result_df)
            self.plot_minus_log_p_heatmap(result_df)






