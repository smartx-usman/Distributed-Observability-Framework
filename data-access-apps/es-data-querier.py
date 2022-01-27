#! /usr/bin/env python3
"""
For accessing Elasticsearch data.
Author: Muhammad Usman
Version: 0.1.0
"""

import argparse as ap
import logging
import sys

import requests
from requests.structures import CaseInsensitiveDict

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def parse_arguments():
    """Read and parse commandline arguments"""
    parser = ap.ArgumentParser(prog='data_access_api', usage='%(prog)s [options]', add_help=True)
    parser.add_argument('-e', '--elasticsearch_host', nargs=1, help='Elasticsearch Host URL', required=True)
    parser.add_argument('-p', '--elasticsearch_port', nargs=1, help='Elasticsearch Host port', required=True)
    parser.add_argument('-i', '--index', nargs=1, help='Elasticsearch index name to get data from', required=True)
    parser.add_argument('-r', '--records', nargs=1, help='No. of records to fetch', required=True)
    parser.add_argument('-st', '--start_timestamp', nargs=1, help='Start time range in epoch milliseconds',
                        required=True)
    parser.add_argument('-et', '--end_timestamp', nargs=1, help='End time range in epoch milliseconds', required=True)
    #parser.add_argument('-o', '--output_file', nargs=1, help='Output file name', required=True)

    return parser.parse_args(sys.argv[1:])


def get_elasticsearch_data():
    """Get and Process Monitoring data from Elasticsearch"""
    logging.info('Welcome to Querying Elasticsearch DataStore')

    url = f'http://{arguments.elasticsearch_host[0]}:{arguments.elasticsearch_port[0]}/{arguments.index[0]}/_search?size={arguments.records[0]}&pretty'.strip()

    logging.info(f'URL to query {url}')

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    # data = '{"query": {"match_all": {}}}'
    data = '{"query": {"range" : {"@timestamp" : {"gte" : ' \
          + arguments.start_timestamp[0] + ', "lte" : ' \
          + arguments.end_timestamp[0] + ', "boost" : 2.0}}}}'

    telegraf_disk_data = '{"query": { \
    "bool": { \
      "must_not": [ \
        { "match": { "device": "mapper/ubuntu--vg-ubuntu--lv" }} \
      ] , \
      "filter": [  \
        { "range": { "@timestamp" : {"gte" : ' + arguments.start_timestamp[0] + ', "lte" : ' + arguments.end_timestamp[
        0] + ', "boost" : 2.0}}} \
      ] \
    } \
    }}'

    try:
        json_data = requests.get(url, headers=headers, data=data)
        logging.info(f'Querying Status {json_data.status_code}')

    except Exception as exception:
        logging.error(f'Error while getting data from Elasticsearch -> {exception}')

    try:
        with open(f'/data/{arguments.index[0]}.json', 'wb') as json_file:
            json_file.write(json_data.content)
    except Exception as exception:
        logging.error(f'Error while saving data -> {exception}')


# Parse input arguments
arguments = parse_arguments()

# Process data
get_elasticsearch_data()

logging.info(f'Process completed.')

# How to run this program
# python3 es-data-querier.py -e 172.16.23.1 -p 30010 -r 5 -i telegraf_disk_index -st 1643187600000 -et 1643273999000 -o out.csv



