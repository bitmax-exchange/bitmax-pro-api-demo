import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--symbol", type=str, default="BTMX/USDT")
@click.option("--interval", type=str, default="1")
@click.option("--n", type=int, default=10)
@click.option("--frm", type=int, default=None)
@click.option("--to", type=int, default=None)
@click.option("--config", type=str, default="config.json")
def run(symbol, interval, n, frm, to, config):

    btmx_cfg = load_config(get_config_or_default(config))['bitmax']

    host = btmx_cfg['https']
    url = f"{host}/api/pro/barhist"
    params = {"symbol": symbol, "interval": interval, "n": n, "from": frm, "to": to}

    res = requests.get(url, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
