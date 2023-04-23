import sys
from argparse import ArgumentParser

from .t_test import TTest

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--mutations-path", dest="mutations_path", type=str, default="../data/Mutations.tsv",
                        help="Path to mutations file")
    parser.add_argument("--gene-ko-path", dest="gene_ko_path", type=str, default="../data/Gene_KOs.tsv",
                        help='Path to Gene KO file')
    parser.add_argument("--out-path", dest="out_path", type=str, required=True,
                        help="Path to write out results for t test for each mutation, gene KO pair")
    parser.add_argument("--plot", dest="plot", action='store_true',
                        help="Produce heatmap of t statistics and P values for T Test results")

def main():
    opt = parse_args()

    t_test_calculator = TTest(mutations_path = mutations_path,
                            gene_ko_path = gene_ko_path,
                            out_path = out_path,
                            plot = plot)

if __name__ == "__main__":
    main()
