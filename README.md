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

This should generate the `run_gold_fits.sh` and `run_all20k_fits.sh` scripts, which can then be split up and sent to job arrays on a SLURM cluster; e.g., with [disbatch](https://github.com/flatironinstitute/disBatch) (each line runs a binary fit for one system).
