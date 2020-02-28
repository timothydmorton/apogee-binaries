from pathlib import Path
import os
import sys

sys.path.append("..")

from analysis.catalog import get_catalog


# write ini files
for dataset in ["gold", "all20k"]:
    catalog = get_catalog(filename=f"../data/{dataset}_photometry.hdf")
    results_root = Path(f"../results_{dataset}")
    catalog.write_ini(N=2, root=results_root)

    # write overall script
    with open(f"run_{dataset}_fits.sh", "w") as fout:
        for i in catalog.df.index:
            path = Path(f"../results_{dataset}/{str(i)[:2]}/{i}").absolute()
            path.mkdir(parents=True, exist_ok=True)
            line = f"starfit {path} --binary --fehprior flat\n"
            fout.write(line)
