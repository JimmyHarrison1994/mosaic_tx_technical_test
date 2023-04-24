from unittest import TestCase
import pandas as pd
import os
import glob

from t_test.t_test import TTest

data_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../data/"))
results_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../results/"))


def generate_t_test_calculator():
    return TTest(os.path.join(data_dir, "Mutations.tsv"),
                os.path.join(data_dir,"Gene_KOs.tsv"),
                'output.tsv')

def generate_t_test_calculator_plot():
    return TTest(os.path.join(data_dir, "Mutations.tsv"),
                os.path.join(data_dir,"Gene_KOs.tsv"),
                'output.tsv',
                plot=True)
    

class TestIO(TestCase):
    def test_read_data(self):
        t_test_calculator = generate_t_test_calculator()
        merged_df = t_test_calculator._read_data()
        self.assertEqual(merged_df.shape, (17, 21))

    def test_assign_columns(self):
        true_mutation_cols = pd.read_csv(os.path.join(data_dir, "Mutations.tsv"), sep='\t').Mutation.tolist()
        true_gene_ko_cols = list(pd.read_csv(os.path.join(data_dir,"Gene_KOs.tsv"), sep='\t'))[1:]

        t_test_calculator = generate_t_test_calculator()
        merged_df = t_test_calculator._read_data()
        mutations_cols, gene_ko_cols = t_test_calculator._assign_columns(merged_df.columns)

        self.assertEqual(mutations_cols, true_mutation_cols)
        self.assertEqual(gene_ko_cols, true_gene_ko_cols)

class TestTTest(TestCase):
    def test_t_test(self):
        t_test_calculator = generate_t_test_calculator()
        merged_df = t_test_calculator._read_data()

        t_test_results = t_test_calculator._t_test(merged_df, 'Gene1_mut', 'GeneA_KO')
        self.assertAlmostEqual(t_test_results[0], -0.2728, places=4)
        self.assertAlmostEqual(t_test_results[1], 0.7887, places=4)

    def test_write_data(self):
        for file in glob.glob(os.path.join(results_dir, '*')):
            os.remove(file)
            
        t_test_calculator = generate_t_test_calculator()
        t_test_calculator.main()

        self.assertEqual(os.listdir(results_dir), ['output.tsv'])

        results_df = pd.read_csv(os.path.join(results_dir, 'output.tsv'), sep='\t')
        self.assertEqual(results_df.shape, (100, 4))

    def test_plot(self):
        for file in glob.glob(os.path.join(results_dir, '*')):
            os.remove(file)

        t_test_calculator = generate_t_test_calculator_plot()

        t_test_calculator.main()

        output_files = os.listdir(results_dir)
        output_files.sort()
        self.assertEqual(output_files, ['output.tsv', 'p_value_heatmap.png', 't_statistic_heatmap.png'])






