import os

import json
import requests

import pandas as pd

_dir_pkg_root = os.path.dirname(__file__)


def load_secrets():
    fn_secrets = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "fantrax.secrets",
    )
    with open(fn_secrets, "r") as fsecrets:
        secrets = json.load(fsecrets)
    return secrets


def dump_to_json(fn_json, data):
    with open(fn_json, "w") as f_json:
        json.dump(data, f_json, indent=4)


def rest_request(
    url,
    body,
    note="",
    resp_format="json",
):
    if resp_format == "json":
        headers = {"Content-Type": "application/json"}
    elif resp_format == "csv":
        headers = {"Content-Type": "application/csv"}

    response = requests.post(
        url,
        data=json.dumps(body),
        headers=headers,
    )
    print(f"{note}status code:", response.status_code)

    if resp_format == "json":
        return response.json()
    elif resp_format == "csv":
        return response.text
    else:
        return response


def load_playerIDMap():
    fn_IDmap = os.path.join(_dir_pkg_root, "data", "PLAYERIDMAP.csv")
    print("\nloading player ID map... ", end="", flush=True)
    df_datamap = pd.read_csv(fn_IDmap)
    print("done.")
    return df_datamap
