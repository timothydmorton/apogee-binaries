# apogee-binaries

Testing fitting binary-star photometry on APOGEE RV-detected binary stars.

## Requirements

Make sure you are on current master of **isochrones**.
Clone this repository into somewhere that 

## Setting up isochrones .ini files and scripts

```
cd scripts
python prepare.py
```

This should generate the `run_gold_fits.sh` and `run_all20k_fits.sh` scripts, which can then be split up and sent to job arrays on a SLURM cluster; e.g., with [disbatch](https://github.com/flatironinstitute/disBatch) (each line runs a binary fit for one system).  These scripts should look something like this (with absolute path depending on your system, of course):
```
(isochrones) Timothys-MacBook-Pro:scripts tmorton$ head -3 run_gold_fits.sh run_all20k_fits.sh
==> run_gold_fits.sh <==
starfit /Users/tmorton/repositories/testing/apogee-binaries/results_gold/3/306768039864448 --binary --fehprior flat
starfit /Users/tmorton/repositories/testing/apogee-binaries/results_gold/9/9999444075159936 --binary --fehprior flat
starfit /Users/tmorton/repositories/testing/apogee-binaries/results_gold/6/65194584193758336 --binary --fehprior flat

==> run_all20k_fits.sh <==
starfit /Users/tmorton/repositories/testing/apogee-binaries/results_all20k/42/420936967163609728 --binary --fehprior flat
starfit /Users/tmorton/repositories/testing/apogee-binaries/results_all20k/53/539684085514189312 --binary --fehprior flat
starfit /Users/tmorton/repositories/testing/apogee-binaries/results_all20k/43/431771039351005184 --binary --fehprior flat
```
