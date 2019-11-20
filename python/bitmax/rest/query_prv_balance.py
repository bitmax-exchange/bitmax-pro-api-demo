import click
import requests
from pprint import pprint
from bitmax.util.auth import *


@click.command()
@click.option("--asset", type=str, default=None,
              help='optional, if none, return all assets with non-empty balance. You can specify an asset (e.g. "BTC")')
@click.option("--account", type=str, default="cash", help="cash (default) or margin")
@click.option("--config", type=str, default="../config/config.json", help="path to the config file")
def run(asset, account, config):
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "balance", apikey, secret)
    url = f"{host}/{group}/api/pro/{account}/balance"

    params = dict(asset=asset)

    res = requests.get(url, headers=headers, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
