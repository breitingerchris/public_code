# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import requests
import requests.exceptions
import urllib
import re
import concurrent.futures
import os
import json


if __name__ == '__main__':
    # cookie = raw_input('Steam Cookie: ')
    item = raw_input('Item to search: ')
    price = raw_input('Price to buy: ')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
    }
    render = requests.get(
        'http://steamcommunity.com/market/search/render/?query={0}&start=0&count=10'.format(
            urllib.quote_plus(item)
        )
    )
    print json.loads(render.text)