import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *



@click.command()
@click.option("--symbol", type=str,
              help="If not provided, return tickers of all symbols. You can provide one or more symbols, "
                   "use comma to separate multiple symbols.")
@click.option("--config", type=str, default=None)
def run(symbol, config):
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmxCfg = load_config(config)['bitmax']

    host = btmxCfg['https']

    url = f"{host}/api/pro/ticker"
    params = dict(symbol=symbol)
    print(url)
    print(params)

    res = requests.get(url, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
