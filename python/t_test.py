import pandas as pd
import matplotlib.pyplot as pyplot
import seaborn as sns

from scipy.stats import ttest_ind

class TTest:
    
    def __init__(
        self,
        mutations_path,
        gene_ko_path,
        out_path,
        plot=False
    )
    self.mutations_path = mutations_path
    self.gene_ko_path = gene_ko_path
    self.out_path = out_path
    self.plot = plot

    def _read_mutations_file(self):
        mutations_df = pd.read_csv(self.mutations_path, sep='\t')
        return mutations_df.set_index('Mutation').transpose().reset_index(names=['Model'])

    def _read_gene_ko_file(self):
        return pd.read_csv(self.gene_ko_path)

    def _merge_mutations_gene_ko_dfs(self, mutations_df, gene_ko_df):
        return gene_ko_df.merge(mutations_df, 'inner', on='Model')

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
        sns.heatmap(t_statistic_df, cmap='vlag', center=0, ax = ax)
        ax.set_ylabel('Mutation')
        ax.set_xlabel('Gene KO')
        fig.tight_layout()
        fig.savefig('t_statistic_heatmap.png')

    def plot_minus_log_p_heatmap(self, result_df):
        minus_log_p_df = df.pivot(index='mutation', columns = 'gene_ko', values='p_value').applymap(np.log10) * -1
        fig, ax = plt.subplots(1,1)
        sns.heatmap(minus_log_p_df, cmap='vlag', center=0, ax = ax, cbar_kws={'label': r"$-\mathrm{log}_{10}P$"})
        ax.set_ylabel('Mutation')
        ax.set_xlabel('Gene KO')
        fig.tight_layout()
        fig.savefig('p_value_heatmap.png')


    def main(self):
        mutations_df = self._read_mutations_file()
        mutations_cols = [x for x in mutations_df.cols if 'mut' in x]

        gene_ko_df = self._read_gene_ko_file()
        gene_ko_cols = [x for x in mutations_df.cols if 'KO' in x]

        merged_df = _merge_mutations_gene_ko_dfs(mutations_df, gene_ko_df)

        row_list = []
        for mutation in mutations_cols:
            for gene_ko in gene_ko_cols:
                row_list.append(self._populate_row(merged_df, mutation, gene_ko))

        result_df = pd.DataFrame(row_list)
        result_df.to_csv(self.out_path, sep='\t', index=False)

        if self.plot:
            self.plot_t_statistic_heatmap(result_df)
            self.plot_minus_log_p_heatmap(result_df)






