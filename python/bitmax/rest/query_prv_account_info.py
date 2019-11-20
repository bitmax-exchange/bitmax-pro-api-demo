import click
import requests
from pprint import pprint
from bitmax.util.auth import *


@click.command()
@click.option("--config", type=str, default="config.json", help="path to the config file")
def run(config):
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "info", apikey, secret)
    url = f"{host}/api/pro/info"

    res = requests.get(url, headers=headers)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
