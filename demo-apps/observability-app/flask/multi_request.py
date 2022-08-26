#!/usr/bin/env python3
import argparse as ap
import sys
from concurrent.futures import ThreadPoolExecutor

import requests


def parse_arguments():
    """Read and parse commandline arguments"""
    parser = ap.ArgumentParser(prog='multi_request', usage='%(prog)s [options]', add_help=True)
    parser.add_argument('-a', '--address', nargs=1, help='Web host ip address', required=True)
    parser.add_argument('-d', '--database', nargs=1, help='Database to store data. I.g. mysql|cassandra', required=True)
    parser.add_argument('-n', '--namespace', nargs=1, help='Namespace where database is running.', required=True)
    parser.add_argument('-s', '--size', nargs=1, help='Data size to sort.', required=True)
    parser.add_argument('-l', '--algorithm', nargs=1, help='Sorting algorithm. I.e., merge|quick', required=True)
    parser.add_argument('-r', '--requests', nargs=1, help='Number of requests to send.', required=True)

    return parser.parse_args(sys.argv[1:])


def get_url(url):
    return requests.get(url)


# Parse input arguments
arguments = parse_arguments()

url = f'http://{arguments.address[0]}:30101/sorting?namespace={arguments.namespace[0]}&size={arguments.size[0]}&start=1&end=1000&kind={arguments.algorithm[0]}&store={arguments.database[0]}&database=flask'
print(url)

# list_of_urls = ["http://x.x.x.x:30101/drop_database?namespace=uc1&database=flask"] * 1
# list_of_urls = ["http://x.x.x.x:30101/create_database?namespace=uc1&database=flask"] * 1
list_of_urls = [url] * int(arguments.requests[0])

n_threads = len(list_of_urls)

with ThreadPoolExecutor(max_workers=n_threads) as pool:
    response_list = list(pool.map(get_url, list_of_urls))

for response in response_list:
    print(response)

# How to run this tool
# python3 demo-apps/observability-app/flask/multi_request.py -a x.x.x.x -d mysql -s 1000 -l merge -n uc1 -r 2
