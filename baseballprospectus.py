import os
import json
from warnings import warn

import numpy as np
import pandas as pd

from utils import _dir_pkg_root, load_playerIDMap


def load_baseballprospectus_data(percentile=50):
    _valid_percentiles = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]
    assert (
        percentile in _valid_percentiles
    ), f"percentile not in PECOTA sheets. pick one of {_valid_percentiles}"
    print("loading PECOTA hitting... ", end="", flush=True)
    fn_pecota_hitting = os.path.join(
        _dir_pkg_root,
        "data",
        "pecota2024_hitting_mar11.xlsx",
    )
    df_pecota_hitting = pd.read_excel(
        fn_pecota_hitting,
        sheet_name=f"{percentile:d}",
    )
    df_pecota_hitting["percentile"] = 50.0
    print("done.")
    print("loading PECOTA pitching... ", end="", flush=True)
    fn_pecota_pitching = os.path.join(
        _dir_pkg_root,
        "data",
        "pecota2024_pitching_mar11.xlsx",
    )
    df_pecota_pitching = pd.read_excel(
        fn_pecota_pitching,
        sheet_name=f"{percentile:d}",
    )
    df_pecota_pitching["pos"] = "P"
    df_pecota_pitching.loc[(df_pecota_pitching.gs > (df_pecota_pitching.sv + df_pecota_pitching.hld)), "pos"] = "SP"
    df_pecota_pitching.loc[(df_pecota_pitching.gs < (df_pecota_pitching.sv + df_pecota_pitching.hld)), "pos"] = "RP"
    df_pecota_pitching["percentile"] = 50.0
    print("done.")

    # stash ratios
    total_b1 = np.sum(df_pecota_hitting.b1)
    total_b2 = np.sum(df_pecota_hitting.b2)
    total_b3 = np.sum(df_pecota_hitting.b3)
    total_hr = np.sum(df_pecota_hitting.hr)
    total_h = total_b1 + total_b2 + total_b3 + total_hr

    fn_ratios = os.path.join(
        _dir_pkg_root,
        "data"
        "bp_derived.json",
    )
    with open(fn_ratios, "w") as f_ratios:
        json.dump(
            {
                "b1/h": total_b1/total_h,
                "b2/h": total_b2/total_h,
                "b3/h": total_b3/total_h,
                "hr/h": total_hr/total_h,
            },
            f_ratios,
        )

    return df_pecota_hitting, df_pecota_pitching


def append_fantraxIDs(df_in, df_idmap):
    df_idmap = df_idmap[
        [
            "MLBID",
            "FANTRAXID",
        ]
    ].rename(
        columns={
            "MLBID": "mlbid",
            "FANTRAXID": "fantraxid",
        },
    )
    df_idmap.fantraxid = [str(x) for x in df_idmap.fantraxid]
    df_in = df_in.merge(
        df_idmap,
        on="mlbid",
    )

    return df_in

def append_fantrax_scoring(df_in, pitching=False):
    fn_scoring = os.path.join(
        _dir_pkg_root,
        "data",
        "scoring_" + ("pitching" if pitching else "hitting") + ".json",
    )

    with open(fn_scoring, "r") as f_scoring:
      scoring = json.load(f_scoring)

    # add the fantasy points projection
    df_in["fpts"] = 0.0

    # where we don't have data on a count stat, get global ratios to help fill in the gap
    fn_ratios = os.path.join(
        _dir_pkg_root,
        "data"
        "bp_derived.json",
    )
    with open(fn_ratios, "r") as f_ratios:
        ratios = json.load(f_ratios)

    k_missing = []

    for k, v in scoring.items():
        if k in df_in.columns:
            df_in.fpts += v*df_in[k]
        elif k == "er":
            df_in.fpts += v*(df_in.era/(df_in.ip/9.0))
        elif pitching and (k == "1b"):
            df_in.fpts += v*df_in["h"]*ratios["b1/h"]
        elif pitching and (k == "2b"):
            df_in.fpts += v*df_in["h"]*ratios["b2/h"]
        elif pitching and (k == "3b"):
            df_in.fpts += v*df_in["h"]*ratios["b3/h"]
        else:
            k_missing.append(k)
    print(f"warning: {k_missing} not in {'pitching' if pitching else 'hitting'} dataframe.")

    return df_in

def merge_hittingpitching(df_pecota_hitting, df_pecota_pitching, has_fantrax=True):

  df_pecota_all = df_pecota_hitting.merge(
    df_pecota_pitching.drop(
        [
            'bpid', 'mlbid', 'model_timestamp', 'percentile', 'birthday', 'bats', 'throws', 'height', 'weight', 'season',
            'team', 'age',
        ],
        axis=1,
    ),
    how="outer",
    on=['fantraxid', 'name', 'first_name', 'last_name'] if has_fantrax else ['bpid', 'name', 'first_name', 'last_name'],
    suffixes=["_hit","_pitch"],
  )
  for col_name in [
    'pa', 'g_hit', 'ab', 'r', 'b1', 'b2',
    'b3', 'hr_hit', 'h_hit', 'tb', 'rbi', 'bb_hit', 'hbp_hit', 'so_hit', 'sb', 'cs', 'avg',
    'obp', 'slg', 'babip_hit', 'drc_plus', 'brr', 'drp', 'vorp', 'warp_hit',
    'drp_str', "fpts_hit",
    'w', 'l', 'sv', 'hld', 'g_pitch', 'gs', 'qs', 'bf', 'ip',
    'h_pitch', 'hr_pitch', 'bb_pitch', 'hbp_pitch', 'so_pitch', 'bb9', 'so9', 'gb_percent',
    'babip_pitch', 'whip', 'era', 'fip', 'cfip', 'dra', 'dra_minus', 'warp_pitch', "fpts_pitch"]:
    if col_name in ["fpts_hit", "fpts_pitch"] and not has_fantrax: continue
    df_pecota_all[col_name] = df_pecota_all[col_name].fillna(0)
  df_pecota_all['warp'] = df_pecota_all['warp_hit'] + df_pecota_all['warp_pitch']
  if has_fantrax:
      df_pecota_all['fpts'] = df_pecota_all['fpts_hit'] + df_pecota_all['fpts_pitch']
      df_pecota_all.fantraxid = df_pecota_all.fantraxid[1:-2]
  return df_pecota_all
