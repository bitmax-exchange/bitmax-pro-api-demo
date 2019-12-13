import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--asset", type=str, default=None,
              help='optional, if none, return all assets with non-empty balance. You can specify an asset (e.g. "BTC")')
@click.option("--account", type=str, default="cash", help="cash (default) or margin")
@click.option("--config", type=str, default="config.json", help="path to the config file")
def run(asset, account, config):

    btmx_cfg = load_config(get_config_or_default(config))['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "balance", apikey, secret)
    url = f"{host}/{group}/{ROUTE_PREFIX}/{account}/balance"
    print(f"url = {url}")

    params = dict(asset=asset)

    res = requests.get(url, headers=headers, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
