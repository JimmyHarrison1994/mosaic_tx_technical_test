# mosaic_tx_technical_test

The statistical test chosen to test for an association between presence of a cancer driver mutation and cell count fold change in a CRISPR knockout of a given gene was an independent T-test

## Set up

First make a directory for the results

```
mkdir results
```

To build the docker image run the command

```
docker build -t t_test_image .
```

Then to run the tool run the command 

```
docker run -v $(pwd)/results:/mosaic_tx/results -it t_test_image python -m t_test --out-path t_test_output.tsv --plot
```

This will populate the `results` directory with an output tsv file, containing the t statistic and P-value for each variant, gene pair, and two heatmaps of the t statistics and P-values of each pairwise T-test

A full description of available command line arguments can be given with the command

```
docker run -it t_test_image python -m t_test --help
```

## Interpretation

The only variant, gene pair with a nominally significant association is (P < 0.05) is `Gene6_mut` and `GeneG_KO`. The negative t statistic indicates that carriers of Gene6_mut had a higher cell count fold change than non-carriers and thus this variant potentially increases resistance to knockout of GeneG. However, this association does not pass Bonferroni correction for multiple testing.

## Testing

Unit testing can be run by running the command

```
# Launch an interactive shell script in the Docker image
docker run -it t_test_image /bin/bash

# Navigate to the root directory

cd ..

# Run the tests

pytest
```