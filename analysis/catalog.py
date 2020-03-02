import os
from pathlib import Path

import pandas as pd
import numpy as np

from isochrones.catalog import StarCatalog


def get_catalog(dataset="gold", props=["parallax"], bands=["G", "BP", "RP", "J", "H", "K"]):

    path = Path(f"/{dataset}_photometry.hdf")

    df = pd.read_hdf(path)

    column_map = dict(
        GAIA_PHOT_G_MEAN_MAG="G_mag",
        GAIA_PHOT_BP_MEAN_MAG="BP_mag",
        GAIA_PHOT_RP_MEAN_MAG="RP_mag",
        J="J_mag",
        J_ERR="J_mag_unc",
        H="H_mag",
        H_ERR="H_mag_unc",
        K="K_mag",
        K_ERR="K_mag_unc",
        IRAC_3_6="IRAC_3.6_mag",
        IRAC_3_6_ERR="IRAC_3.6_mag_unc",
        IRAC_5_8="IRAC_5.8_mag",
        IRAC_5_8_ERR="IRAC_5.8_mag_unc",
        WISE_4_5="W2_mag",
        WISE_4_5_ERR="W2_mag_unc",
        GAIA_PARALLAX_ERROR="parallax_unc",
        GAIA_PARALLAX="parallax",
    )

    df = df.rename(columns=column_map)

    # Gaia mag uncertainties (http://gaia.ari.uni-heidelberg.de/gaia-workshop-2018/files/Gaia_DR2_photometry.pdf, slide 27)
    gaia_sys_unc = 0.02

    if "phot_g_mean_flux_over_error" in df:
        df["G_mag_unc"] = np.sqrt((1.086 / df["phot_g_mean_flux_over_error"]) ** 2 + gaia_sys_unc ** 2)
        df["BP_mag_unc"] = np.sqrt((1.086 / df["phot_bp_mean_flux_over_error"]) ** 2 + gaia_sys_unc ** 2)
        df["RP_mag_unc"] = np.sqrt((1.086 / df["phot_rp_mean_flux_over_error"]) ** 2 + gaia_sys_unc ** 2)
    else:
        df["G_mag_unc"] = gaia_sys_unc
        df["BP_mag_unc"] = gaia_sys_unc
        df["RP_mag_unc"] = gaia_sys_unc

    # Gaia parallax offsets/errors (https://www.aanda.org/articles/aa/full_html/2019/08/aa35765-19/T1.html)
    bright = df["G_mag"] < 14
    medium = np.logical_and(df["G_mag"] < 16.5, df["G_mag"] > 14)
    faint = 16.5 < df["G_mag"]

    df.loc[bright, "parallax"] += 0.05
    df.loc[medium, "parallax"] += 0.1676 - 0.0084 * df.loc[medium, "G_mag"]
    df.loc[faint, "parallax"] += 0.029

    bright = df["G_mag"] < 11
    medium = np.logical_and(df["G_mag"] < 15, df["G_mag"] > 11)
    faint = 15 < df["G_mag"]

    df.loc[bright, "parallax_unc"] = df.loc[bright, "parallax_unc"] * 1.2
    df.loc[medium, "parallax_unc"] = df.loc[medium, "parallax_unc"] * (0.22 * df.loc[medium, "G_mag"] - 1.22)
    df.loc[faint, "parallax_unc"] = df.loc[faint, "parallax_unc"] * (
        np.exp(-(df.loc[faint, "G_mag"] - 15)) + 1.08
    )

    df.index = df.GAIA_SOURCE_ID

    cat = StarCatalog(df, props=props, bands=bands)

    return cat
