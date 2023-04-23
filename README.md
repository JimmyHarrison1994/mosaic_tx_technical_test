# mosaic_tx_technical_test

The statistical test chosen to test for an association between presence of a cancer driver mutation and cell count fold change in a CRISPR knockout of a given gene was an independent T-test

## Set up

To build the docker image run the command

```
docker build -t t_test_image .
```

Then to run the tool run the command 

```
docker run -v $(pwd)/results:/results -it t_test_image python -m t_test --out-path t_test_output.tsv --plot
```

This will populate the `results` directory with an output tsv file, containing the t statistic and P-value for each variant, gene pair, and two heatmaps of the t statistics and P-values of each pairwise T-test

