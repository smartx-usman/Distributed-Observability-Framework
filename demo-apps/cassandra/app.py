import logging
import subprocess

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandrapass')
cluster = Cluster(['cassandra.uc1.svc.cluster.local'],
                  auth_provider=auth_provider, protocol_version=3)

try:
    session = cluster.connect()
except Exception as ex:
    logging.error(f'Problem while connecting to Casandra.')

try:
    session.execute(f'DROP keyspace IF EXISTS library;')
    logging.info("Creating keyspace...")
    session.execute(
        "CREATE KEYSPACE library WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")
    logging.info(f'Created keyspace library.')
except Exception as ex:
    logging.error(f'Problem while dropping or creating library keyspace.')

try:
    session = cluster.connect('library')
except Exception as ex:
    logging.error(f'Problem while connecting to Casandra.')

query_book_table = '''
CREATE TABLE library.book (
ISBN text,
copy int,
title text,
PRIMARY KEY (ISBN, copy)
);'''

query_book_table_index = '''
create index on library.book (title);
'''

try:
    session.execute(query_book_table)
except Exception as ex:
    logging.info(f'Table already exists. Not creating.')

try:
    session.execute(query_book_table_index)
except Exception as ex:
    logging.info(f'Index already exists. Not creating.')

try:
    with subprocess.Popen(
            "apache-cassandra-4.0.4/tools/bin/cassandra-stress user profile=stress.yaml ops\(insert=1,books=1\) n=10000  "
            "-graph file=stress.html -node cassandra.uc1.svc.cluster.local "
            "-port native=9042 jmx=7199 "
            "-mode native cql3 user=cassandra password=cassandrapass",
            stdout=subprocess.PIPE,
            shell=True, bufsize=1) as proc:
        for line in proc.stdout:
            logging.info(line.decode('UTF-8'))
        #char = proc.stdout.read(1)
        #while char != b'':
        #    logging.info(char.decode('UTF-8'), end='', flush=True)
        #    char = proc.stdout.read(1)

    # try:
    #outs, errs = proc.communicate(timeout=5)
    # except subprocess.TimeoutExpired:
    #    proc.kill()

except Exception as ex:
    logging.info(f'Run stress test failed. {ex}')
