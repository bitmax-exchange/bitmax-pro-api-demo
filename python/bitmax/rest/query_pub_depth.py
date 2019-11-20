import click
import requests
from pprint import pprint
from bitmax.util.auth import *


@click.command()
@click.option("--symbol", type=str, default="BTMX/USDT")
@click.option("--config", type=str, default="../config/config.json")
def run(symbol, config):
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']

    url = f"{host}/api/pro/depth"
    params = dict(symbol=symbol)

    print(url)
    res = requests.get(url, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
