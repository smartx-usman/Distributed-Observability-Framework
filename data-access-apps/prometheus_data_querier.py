import requests
import sys
from csv import writer


def GetMetrixNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']
    # Return metrix names
    return names


def query_metrics(metric, start_timestamp, end_timestamp, namespace, step, type, filter_container, output_file):
    """Query metrics from Prometheus and write to csv file."""
    write_header = True
    # 'http://10.102.141.236/api/v1/query_range?query=kubernetes_pod_container_memory_usage_bytes&start=2022-06-21T08:20:00.000Z&end=2022-06-21T08:25:00.000Z&step=10s'

    if type == 'query':
        container = 'telegraf'
        query_url = f'http://' + sys.argv[
            1] + '/api/v1/query_range?query=' + metric + '{namespace=\"' + namespace + '\", container_name=\"' + filter_container + '\"}&start=' + start_timestamp + '&end=' + end_timestamp + '&step=' + step

    if type == 'rate':
        query_url = f'http://' + sys.argv[1] + '/api/v1/query_range?query=rate(' + sys.argv[
            2] + '{namespace=\"' + sys.argv[6] + '\"})&start=' + sys.argv[3] + '&end=' + sys.argv[4] + '&step=' + \
                   sys.argv[
                       5]
    print(query_url)

    response = requests.get(query_url)
    results = response.json()['data']['result']

    # Build a list of all label names used. Gets all keys and discard __name__
    label_names = set()
    for result in results:
        label_names.update(result['metric'].keys())

    # Canonicalize
    label_names.discard('__name__')
    label_names = sorted(label_names)

    # Write the samples.
    with open(output_file, 'a') as writer_object:
        csv_writer = writer(writer_object)
        if write_header:
            csv_writer.writerow(['name', 'timestamp', 'value'] + label_names)
            write_header = False

        for result in results:
            l = [result['metric'].get('__name__', '')]

            for label in label_names:
                l.append(result['metric'].get(label, ''))

            for rec in result['values']:
                if type == 'query':
                    final_row = [str(l[0]), str(rec[0]), str(rec[1]), str(l[1]), str(l[2]), str(l[3]), str(l[4]),
                                 str(l[5]), str(l[6]), str(l[7])]
                else:
                    final_row = str(l[0]) + ',' + str(rec[0]) + ',' + str(rec[1]) + ',' + str(l[2]) + ',' + str(
                        l[3]) + ',' + str(l[4]) + ',' + str(l[5]) + ',' + str(l[6])  # + ',' + str(l[7])

                # print(final_row)
                csv_writer.writerow(final_row)


def main():
    """Main function."""
    print(len(sys.argv))
    if len(sys.argv) != 8:
        print('Usage: {0} http://localhost:9090'.format(sys.argv[0]))
        sys.exit(1)

    metrics_list = ["kubernetes_pod_container_memory_usage_bytes", "kubernetes_pod_container_cpu_usage_nanocores"]
    start_timestamp = sys.argv[2]
    end_timestamp = sys.argv[3]
    namespace = sys.argv[4]
    step = sys.argv[5]
    filter_container = sys.argv[6]
    output = sys.argv[7]

    query_metrics(metrics_list[0], start_timestamp, end_timestamp, namespace, step, "query", filter_container, f'telegraf_memory_result_{output}.csv')
    query_metrics(metrics_list[1], start_timestamp, end_timestamp, namespace, step, "query", filter_container, f'telegraf_cpu_result_{output}.csv')

    # metrixNames = GetMetrixNames(sys.argv[1])


if __name__ == '__main__':
    main()

# How to run
# python3 prometheus_data_querier.py 10.102.141.236 kubernetes_pod_container_memory_usage_bytes 2022-06-21T08:20:00.000Z 2022-06-21T08:25:00.000Z 10s | grep 'app\|name' >> result.csv
# python3 prometheus_data_querier.py x.x.x.x:32099 kubernetes_pod_network_tx_bytes 2023-01-02T12:31:01.000Z 2023-01-02T13:29:59.000Z 10s measurement | grep -e 'name' | grep -v -e edge-metrics-analyzer -e promtail -e master>> telegraf_network_result_250ms.csv
# python3 prometheus_data_querier.py x.x.x.x:32099 kubernetes_pod_container_memory_usage_bytes 2023-01-13T12:00:00.000Z 2023-01-13T13:59:59.000Z 10s measurement | grep -e 'name' | grep -v -e rabbitmq -e edge-metrics-analyzer >> loki_mem_result_200-pods.csv
# python3 prometheus_data_querier.py x.x.x.x:32099 kubernetes_pod_container_cpu_usage_nanocores 2023-01-20T14:00:00.000Z 2023-01-20T14:59:59.000Z 10s observability | grep -e 'name' grep -e 'jaeger-agent' >> jaeger_cpu_result_200-pods.csv
# python3 prometheus_data_querier.py x.x.x.x:32099 2023-02-28T13:00:00.000Z 2023-02-28T13:59:59.000Z measurement 10s telegraf 1s