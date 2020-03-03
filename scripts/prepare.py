from pathlib import Path
import os
import sys

sys.path.append("..")

from analysis.catalog import get_catalog

# write ini files
for dataset in ["gold"]:  # , "all20k"]:
    catalog = get_catalog(dataset=dataset)
    results_root = Path(f"../results_{dataset}")
    paths = catalog.write_ini(N=2, root=results_root)

    # write overall script
    with open(f"run_{dataset}_fits.sh", "w") as fout:
        for i, path in zip(catalog.df.index, paths):
            line = f"starfit {path} --binary --fehprior flat\n"
            fout.write(line)
