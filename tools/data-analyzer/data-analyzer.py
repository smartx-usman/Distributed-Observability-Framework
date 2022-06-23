import argparse as ap
import logging
import socket
import subprocess
import sys
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def parse_arguments():
    """Read and parse commandline arguments"""
    parser = ap.ArgumentParser(prog='data-analyzer', usage='%(prog)s [options]', add_help=True)
    parser.add_argument('-n', '--namespace', nargs=1, help='Specify namespace to check', required=True)
    parser.add_argument('-a', '--app_name', nargs=1, help='Specify application name to check', required=True)
    parser.add_argument('-m', '--metric_name', nargs=1, help='Specify metric name to check', required=True)
    parser.add_argument('-v', '--metric_value', nargs=1, help='Specify metric value threshold', required=True)

    return parser.parse_args(sys.argv[1:])


def process_data():
    """Process incoming monitoring data"""

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 65432)

    # logging.info(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        logging.info('waiting for a connection.')
        connection, client_address = sock.accept()

        try:
            # logging.info(sys.stderr, 'connection from', client_address)

            # Receive the data in the chunks
            while True:
                data = connection.recv(8192)
                data = data.decode('utf-8')
                # print(sys.stderr, 'received "%s"' % data)

                metric_name = arguments.metric_name[0]  # 'memory_usage_bytes'
                app_name = arguments.app_name[0]  # 'app-1-pod'

                try:
                    metric_label_array = data.split(" ")[0]
                    metric_data_array = data.split(" ")[1]
                    app_label = (metric_label_array.split(",")[5]).split("=")[1]

                    if app_label == app_name:
                        logging.info(app_label)

                    if app_name in metric_label_array and metric_name in metric_data_array:
                        # if metric_name in metric_data_array:
                        metric_values_array = metric_data_array.split(",")
                        for metric_check in metric_values_array:
                            # logging.info(metric_check)
                            if metric_name == metric_check.split("=")[0]:
                                metric_value = int(metric_check.split("=")[1][:-1])
                                if metric_value <= int(arguments.metric_value[0]):
                                    logging.info(f'{metric_value} is less than threshold. Restarting application.')
                                    p = subprocess.Popen(
                                        "kubectl -n " + arguments.namespace[0] + " rollout restart deploy",
                                        stdout=subprocess.PIPE, shell=True)
                                    logging.info(p.communicate())
                                    time.sleep(60)

                                break

                except Exception as exception:
                    print('')

                # if data:
                #    print(sys.stderr, 'sending data back to the client')
                #    connection.sendall(data)
                # else:
                #    print(sys.stderr, 'no more data from', client_address)
                #    break

        finally:
            # Clean up the connection
            connection.close()


# Parse input arguments
arguments = parse_arguments()

# Process monitoring data
process_data()
