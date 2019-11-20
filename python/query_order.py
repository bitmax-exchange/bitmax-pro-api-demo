import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *



def get_hist_orders(base_url, apikey, secret, symbol, start_time, end_time, order_type, side,
                    method="order/hist/current"):
    ts = utc_timestamp()
    url = "{}/{}".format(base_url, method)
    headers = make_auth_headers(ts, method, apikey, secret)
    params = {"symbol": symbol, "startTime": start_time, "endTime": end_time, "orderType": order_type, "side": side}
    return requests.get(url, headers=headers, params=params)


def get_open_orders(base_url, apikey, secret, symbol, method="order/open"):
    ts = utc_timestamp()
    url = "{}/{}".format(base_url, method)
    headers = make_auth_headers(ts, method, apikey, secret)
    params = {"symbol": symbol}
    return requests.get(url, headers=headers, params=params)


def get_order_status(base_url, apikey, secret, coid, method="order/status"):
    url = "{}/{}/{}".format(base_url, method, coid)
    print(url)
    ts = utc_timestamp()
    headers = make_auth_headers(ts, method, apikey, secret)
    return requests.get(url, headers=headers)


@click.command()
@click.option("--account", type=click.Choice(['cash', 'margin']), default="cash")
@click.option("--symbol", type=str, default='BTC/USDT')
@click.option("--start_time", type=int, default=0)
@click.option("--end_time", type=int, default=utc_timestamp())
@click.option("--order_type", type=str, default=None)  # "market" or "limit"
@click.option("--side", type=click.Choice(['buy', 'sell']), default=None)
@click.option("--coid", type=str, default=None)
@click.option("--config", type=str, default=None, help="path to the config file")
def run(account, symbol, start_time, end_time, order_type, side, config, coid):
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    base_url = f"{host}/{group}/api/pro/{account}"

    print("Get history orders")
    res = get_hist_orders(base_url, apikey, secret, symbol, start_time, end_time, order_type=order_type, side=side)
    pprint(parse_response(res))

    print("\n ****** \n")
    print("Get open orders")
    res = get_open_orders(base_url, apikey, secret, None)
    pprint(parse_response(res))

    if coid is not None:
        print("\n ****** \n")
        print(f"Query status for order {coid}")
        res = get_order_status(base_url, apikey, secret, coid)
        pprint(parse_response(res))


if __name__ == "__main__":
    run()
