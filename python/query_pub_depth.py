import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--symbol", type=str, default="BTMX/USDT")
@click.option("--config", type=str, default="config.json")
def run(symbol, config):

    btmx_cfg = load_config(get_config_or_default(config))['bitmax']

    host = btmx_cfg['https']

    url = f"{host}/{ROUTE_PREFIX}/depth"
    params = dict(symbol=symbol)

    print(url)
    res = requests.get(url, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
