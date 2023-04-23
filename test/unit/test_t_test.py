from unittest import TestCase
import pandas as pd

from t_test.t_test import TTest

def generate_t_test_calculator():
    return = TTest("../../data/Mutations.tsv",
                            "../../data/Gene_KO.tsv",
                            'output.tsv')
    

class TestIO(TestCase):
    def test_read_data(self):
        t_test_calculator = generate_t_test_calculator()
        merged_df = t_test_calculator._read_data()
        self.assertEqual(merged_df.shape, (17, 21))

    def test_assign_columns(self):
        true_mutation_cols = pd.read_csv("../../data/Mutations.tsv", sep='\t').Mutation.tolist()
        true_gene_ko_cols = list(pd.read_csv("../../data/Gene_KO.tsv", sep='\t'))[1:]

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



