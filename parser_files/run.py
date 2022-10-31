import os
import random

import yaml

from parser import Parser

if __name__ == '__main__':
    parser = Parser()
    with open(os.path.abspath(os.path.join(os.getcwd(), '..', 'config.yaml'))) as fh:
        read_yaml = yaml.safe_load(fh)
    list_proxies = read_yaml[1]['proxies']
    if not list_proxies:
        search_result = parser.download_json()
    else:
        proxy = random.choice(list_proxies)
        proxies = {
            "http": f"http://{proxy}/",
            "https": f"http://{proxy}/"
        }
        search_result = parser.download_json(proxies=proxies)
