import click
import requests
from pprint import pprint

# Local imports 
from util import *


def cancel_order(order, apikey, secret, base_url, method="order"):
    url = "{}/{}".format(base_url, method)
    ts = utc_timestamp()
    coid = order['coid']
    headers = make_auth_headers(ts, method, apikey, secret, coid=coid)
    return requests.delete(url, headers=headers, json=order)


def cancel_batch_order(orders, apikey, secret, base_url, method="order/batch"):
    url = "{}/{}".format(base_url, method)
    ts = utc_timestamp()
    coid = "+".join([order['coid'] for order in orders])
    batch_order = {"orders": orders}
    headers = make_auth_headers(ts, method, apikey, secret, coid=coid)
    return requests.delete(url, headers=headers, json=batch_order)


def cancel_all_order(symbol, apikey, secret, base_url, method="order/all"):
    print(f"cancel all ${symbol}")
    if symbol is not None:
        params = {"symbol": symbol}
    else:
        params = {}

    url = "{}/{}".format(base_url, method)
    ts = utc_timestamp()
    headers = make_auth_headers(ts, method, apikey, secret)
    return requests.delete(url, headers=headers, params=params)


def test_cancel_batch_order(api_key, secret, base_url):
    ts = utc_timestamp()
    order1 = dict(
        coid=uuid32(),
        origCoid="16e61d5ff43s8bXHbAwwoqDo9d817339",
        time=ts,
        symbol="BTC/USDT",
    )

    order2 = dict(
        coid=uuid32(),
        origCoid="16e61adeee5a8bXHbAwwoqDo100e364e",
        time=ts,
        symbol='ETH/USDT',
    )

    res = cancel_batch_order([order1, order2], api_key, secret, base_url)
    pprint(parse_response(res))


@click.command()
@click.option("--account", type=click.Choice(['cash', 'margin']), default="cash")
@click.option("--order-id", type=str, default=None, help="order id (provided by server when placing order) to cancel")
@click.option("--symbol", type=str, default='BTC/USDT')
@click.option("--resp-inst", type=click.Choice(['ACK', 'ACCEPT', 'DONE']), default="ACK")
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option("--cancel_all", type=bool, default=False, help="set cancel_all to be true to cancel all")
def run(account, order_id, symbol, resp_inst, config, cancel_all):
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    base_url = f"{host}/{group}/api/pro/{account}"

    if cancel_all:
        cancel_all_order(symbol, apikey, secret, base_url)

    else:
        ts = utc_timestamp()
        order = dict(
            coid=uuid32(),
            origCoid=order_id,
            time=ts,
            symbol=symbol.replace("-", "/"),
            respInst=resp_inst,
        )

        print("Cancel order {}".format(order))
        res = cancel_order(order, apikey=apikey, secret=secret, base_url=base_url, method="order")
        pprint(parse_response(res))


if __name__ == "__main__":
    run()
