import argparse as ap
import logging
import os
import pika
import socket
import subprocess
import sys
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def parse_arguments():
    """Read and parse commandline arguments"""
    parser = ap.ArgumentParser(prog='data-analyzer', usage='%(prog)s [options]', add_help=True)
    parser.add_argument('-n', '--namespace', nargs=1, help='Specify namespace to check', required=False, default='uc1')
    parser.add_argument('-a', '--app_name', nargs=1, help='Specify application name to check', required=False,
                        default='app-1-pod')
    parser.add_argument('-m', '--metric_name', nargs=1, help='Specify metric name to check', required=False,
                        default='memory_usage_bytes')
    parser.add_argument('-v', '--metric_value', nargs=1, help='Specify metric value threshold', required=False,
                        default='50000000',)
    parser.add_argument('-r', '--rabbitmq_broker', nargs=1, help='Specify rabbitmq_broker url',
                        required=False,
                        default='amqp://user:user@rabbitmq-headless.observability.svc.cluster.local:5672')

    return parser.parse_args(sys.argv[1:])


def process_data():
    """Process incoming monitoring data via Socket"""

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


def process_data2():
    """Process incoming monitoring data via execd"""
    while True:
        data = sys.stdin.readline()
        logging.info(data)

        metric_name = arguments.metric_name[0]  # 'memory_usage_bytes'
        app_name = arguments.app_name[0]  # 'app-1-pod'

        try:
            metric_label_array = data.split(" ")[0]
            metric_data_array = data.split(" ")[1]
            app_label = (metric_label_array.split(",")[5]).split("=")[1]

            logging.info(app_label)

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

    sys.exit(0)


def process_data_rabbitmq():
    try:
        parameters = pika.URLParameters(arguments.rabbitmq_broker[0])
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        #channel.queue_declare(queue='telegraf')

        channel.exchange_declare(exchange='telegraf', exchange_type='direct')
        result = channel.queue_declare(queue='telegraf-kubernetes', durable=False, exclusive=False)
        queue_name = result.method.queue

        channel.queue_bind(exchange='telegraf', queue=queue_name)

        def callback(ch, method, properties, body):
            logging.info(" [x] Received [%r]" % body)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        logging.info(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.warn('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


# Parse input arguments
arguments = parse_arguments()

# Process monitoring data
process_data_rabbitmq()
