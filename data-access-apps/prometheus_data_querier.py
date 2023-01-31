import csv
import sys

import requests


def GetMetrixNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']
    # Return metrix names
    return names


"""
Prometheus data as csv.
"""
writer = csv.writer(sys.stdout)
if len(sys.argv) != 6:
    print('Usage: {0} http://localhost:9090'.format(sys.argv[0]))
    sys.exit(1)

# metrixNames = GetMetrixNames(sys.argv[1])
writeHeader = True

# 'http://10.102.141.236/api/v1/query_range?query=kubernetes_pod_container_memory_usage_bytes&start=2022-06-21T08:20:00.000Z&end=2022-06-21T08:25:00.000Z&step=10s'
# for metrixName in (kubernetes_pod_container_memory_usage_bytes):
# now its hardcoded for hourly
QuryURL = f'http://' + sys.argv[1] + '/api/v1/query_range?query=' + sys.argv[
    2] + '&start=' + sys.argv[3] + '&end=' + sys.argv[4] + '&step=' + sys.argv[5]
print(QuryURL)

response = requests.get(QuryURL)  # ,
# params={'query': metrixName + '[1h]'})
# kubernetes_pod_container_memory_usage_bytes
# 10.102.141.236
results = response.json()['data']['result']
# Build a list of all labelnames used.
# gets all keys and discard __name__
labelnames = set()
for result in results:
    labelnames.update(result['metric'].keys())

# Canonicalize
labelnames.discard('__name__')
labelnames = sorted(labelnames)

# Write the samples.
if writeHeader:
    writer.writerow(['name', 'timestamp', 'value'] + labelnames)
    writeHeader = False

for result in results:
    l = [result['metric'].get('__name__', '')]

    for label in labelnames:
        l.append(result['metric'].get(label, ''))

    for rec in result['values']:
        final_row = str(l[0]) + ',' + str(rec[0]) + ',' + str(rec[1]) + ',' + str(l[1]) + ',' + str(l[2]) + ',' + str(
            l[3]) + ',' + str(l[4]) + ',' + str(l[5]) + ',' + str(l[6]) + ',' + str(l[7])
        #print(final_row)
        writer.writerow(final_row)

# How to run
# python3 prometheus_data_querier.py 10.102.141.236 kubernetes_pod_container_memory_usage_bytes 2022-06-21T08:20:00.000Z 2022-06-21T08:25:00.000Z 10s | grep 'app\|name' >> result.csv
# python3 prometheus_data_querier.py x.x.x.x:32099 kubernetes_pod_network_tx_bytes 2023-01-02T12:31:01.000Z 2023-01-02T13:29:59.000Z 10s | grep -e 'name' -e 'measurement' | grep -v -e edge-metrics-analyzer -e promtail -e master>> telegraf_network_result_250ms.csv
# python3 prometheus_data_querier.py x.x.x.x:32099 kubernetes_pod_container_memory_usage_bytes 2023-01-13T12:00:00.000Z 2023-01-13T13:59:59.000Z 10s | grep -e 'name' -e 'measurement' | grep -v -e rabbitmq -e edge-metrics-analyzer >> loki_memory_result_200-pods.csv
# python3 prometheus_data_querier.py x.x.x.x:32099 kubernetes_pod_container_cpu_usage_nanocores 2023-01-20T14:00:00.000Z 2023-01-20T14:59:59.000Z 10s | grep -e 'jaeger-agent' >> jaeger_cpu_result_200-pods.csv