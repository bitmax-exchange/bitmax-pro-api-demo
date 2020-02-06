import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *



@click.command()
@click.option("--symbol", type=str, default=None)
@click.option("--account", type=click.Choice(['cash', 'margin']), default="cash", help="account category")
@click.option("--order_id", type=str, default=None)
@click.option("--config", type=str, default="config.json", help="path to the config file")
@click.option("--verbose/--no-verbose", default=False)
def run(symbol, account, order_id, config, verbose):

    btmx_cfg = load_config(get_config_or_default(config))['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "order/status", apikey, secret)
    url = f"{host}/{group}/{ROUTE_PREFIX}/{account}/order/status/{order_id}"
    params = dict(orderId = order_id)

    if verbose:
        print(f"Using url: {url}")
        print(f"params: {params}")


    res = requests.get(url, headers=headers, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
