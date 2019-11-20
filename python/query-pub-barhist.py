import click
import requests
from pprint import pprint
from util.auth import *


@click.command()
@click.option("--symbol", type=str, default="BTMX/USDT")
@click.option("--interval", type=str, default="1")
@click.option("--frm", type=int)
@click.option("--to", type=int)
@click.option("--n", type=int, default=10)
@click.option("--config", type=str, default="config.json")
def run(symbol, interval, frm, to, n, config):
  btmxCfg = load_config(config)['bitmax']

  host   = btmxCfg['https']
  
  url = f"{host}/api/pro/barhist"
  params = {
    "symbol":   symbol,
    "interval": interval,
    "n":        n,
    "from":     frm,
    "to":       to,
  }

  print(url)
  res = requests.get(url, params = params)
  pprint(parse_response(res))


if __name__ == "__main__": 
  run()  


