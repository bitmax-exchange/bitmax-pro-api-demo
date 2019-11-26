import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *
from query_order import get_order_status


BASE_METHOD = "order"
BATCH_METHOD = f"{BASE_METHOD}/batch"


def place_order(order, apikey, secret, base_url, method):
    url = "{}/{}".format(base_url, method)
    ts = utc_timestamp()
    coid = order['coid']
    headers = make_auth_headers(ts, method, apikey, secret)
    return requests.post(url, headers=headers, json=order)


def place_batch_order(orders, api_key, secret, base_url, method=BATCH_METHOD):
    """
    e.g.
    batch_order = [order1, order2]
    print("Place batch order {}".format(batch_order))
    res = place_batch(batch_order, api_key=api_key, secret=secret, base_url=base_url)
    pprint(parse_response(res))

    :param orders:
    :param api_key:
    :param secret:
    :param base_url:
    :param method:
    :return:
    """
    url = "{}/{}".format(base_url, method)
    ts = utc_timestamp()
    coid = "+".join([order['coid'] for order in orders])
    batch_order = {"orders": orders}
    headers = make_auth_headers(ts, method, api_key, secret, coid=coid)

    return requests.post(url, headers=headers, json=batch_order)


@click.command()
@click.option("--account", type=click.Choice(['cash', 'margin']), default="cash")
@click.option("--symbol", type=str, default='BTC/USDT')
@click.option("--price", type=str, default='9500')
@click.option("--qty", type=str, default='0.1')
@click.option("--order_type", type=str, default="market")
@click.option("--side", type=click.Choice(['buy', 'sell']), default='buy')
@click.option("--resp_inst", type=click.Choice(['ACK', 'ACCEPT', 'DONE']), default="DONE")
@click.option("--config", type=str, default=None, help="path to the config file")
def run(account, symbol, price, qty, order_type, side, resp_inst, config):
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    if "account_id" in btmx_cfg:
        account_id = btmx_cfg["account_id"]
    else:
        account_id = None

    base_url = f"{host}/{group}/api/pro/{account}"

    ts = utc_timestamp()
    order = dict(
        coid=uuid32(),
        time=ts,
        symbol=symbol.replace("-", "/"),
        orderPrice=str(price),
        orderQty=str(qty),
        orderType=order_type,
        side=side.lower(),
        respInst=resp_inst,
    )

    print("Place order {} through {}".format(order, base_url))
    res = place_order(order, apikey=apikey, secret=secret, base_url=base_url, method="order")
    pprint(parse_response(res))

    # query order status
    if account_id is not None:
        time.sleep(1)
        coid = order["coid"]
        server_coid = gen_server_order_id(account_id, symbol=order["symbol"], side=order["side"], cl_order_id=coid,
                                          ts=order["time"], order_src='a')
        print(f"server_coid = {server_coid}")
        res = get_order_status(base_url, apikey, secret, server_coid)
        pprint(parse_response(res))


if __name__ == "__main__":
    run()
