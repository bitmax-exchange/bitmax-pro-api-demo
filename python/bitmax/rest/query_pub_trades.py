import click
import requests
from pprint import pprint
from bitmax.util.auth import *


@click.command()
@click.option("--symbol", type=str, default="BTMX/USDT")
@click.option("--n", type=int, default=10, help="number of records to request")
@click.option("--config", type=str, default="../config/config.json")
def run(symbol, n, config):
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']

    url = f"{host}/api/pro/trades"
    params = dict(symbol=symbol, n=n)

    res = requests.get(url, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
