import logging
import socket
import subprocess
import sys
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

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
        logging.info(sys.stderr, 'connection from', client_address)

        # Receive the data in small chunks
        while True:
            data = connection.recv(8192)
            data = data.decode('utf-8')
            # print(sys.stderr, 'received "%s"' % data)
            # print(data + "\n")

            metric_name = 'memory_usage_bytes'
            app_name = 'app-1-pod'

            try:
                metric_label_array = data.split(" ")[0]
                metric_data_array = data.split(" ")[1]
                app_label = (metric_label_array.split(",")[5]).split("=")[1]

                if app_label == app_name:
                    logging.info(app_label)

                if app_name in metric_label_array:
                    if metric_name in metric_data_array:
                        metric_values_array = metric_data_array.split(",")
                        for metric_check in metric_values_array:
                            #logging.info(metric_check)
                            if metric_name == metric_check.split("=")[0]:
                                metric_value = int(metric_check.split("=")[1][:-1])
                                if metric_value <= 50000000:
                                    logging.info(f'Memory {metric_value} is less than threshold. Restarting the '
                                                 f'application.')
                                    p = subprocess.Popen("kubectl -n uc1 rollout restart deploy",
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
