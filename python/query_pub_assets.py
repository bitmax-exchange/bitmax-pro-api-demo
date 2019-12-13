import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *



@click.command()
@click.option("--config", type=str, default="config.json")
def run(config):
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']

    url = f"{host}/{ROUTE_PREFIX}/assets"

    print(f"Using url: {url}")

    res = requests.get(url)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
