import logging
import subprocess
import time
from random import randint

import numpy as np
from flask import Flask, request, jsonify, abort
from flask_mysqldb import MySQL
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

resource = Resource(attributes={
    SERVICE_NAME: "observability-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger-agent.observability.svc.cluster.local",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.uc1.svc.cluster.local'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)


@app.route("/roll")
def roll():
    sides = int(request.args.get('sides'))
    rolls = int(request.args.get('rolls'))
    return roll_sum(sides, rolls)


def roll_sum(sides, rolls):
    with tracer.start_as_current_span("roll_sum") as rollspan:
        # span = trace.get_current_span()
        rollspan.set_attribute('my-tag', 10)
        sum = 0
        for r in range(0, rolls):
            result = randint(1, sides)
            # rollspan.set_attribute('sum', result)
            rollspan.add_event("log", {
                "roll.sides": sides,
                "roll.result": result,
            })
            sum += result
        return str(sum)


@app.route("/multispan")
def multi_span():
    # Create a new span to track some work
    with tracer.start_as_current_span("parent") as parent_span:
        time.sleep(1)
        parent_span.set_attribute('my-tag', 'parent')

        # Create a nested span to track nested work
        with tracer.start_as_current_span("child") as child_span:
            child_span.set_attribute('my-tag', 'child')
            time.sleep(2)
            # the nested span is closed when it's out of scope

        # Now the parent span is the current span again
        time.sleep(1)
    return 'Finished'


@app.route("/matrix-multiplication")
def matrix_multiply():
    # Create a new span to track some work
    start_dt = time.time()
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    rows = int(request.args.get('rows'))
    cols = int(request.args.get('cols'))
    with tracer.start_as_current_span("matrix-multiply") as parent_span:
        with tracer.start_as_current_span("matrix-data-op") as child_span1:
            child_span1.set_attribute('start_range', start)
            child_span1.set_attribute('end_range', end)
            matrix_a = np.random.randint(start, end, size=(rows, cols))
            matrix_b = np.random.randint(start, end, size=(rows, cols))

        # Create a nested span to track nested work
        with tracer.start_as_current_span("matrix-multiply-op") as child_span2:
            result = np.matmul(matrix_a, matrix_b)
            child_span2.set_attribute('rows', rows)
            child_span2.set_attribute('cols', cols)
            # the nested span is closed when it's out of scope

        # Now the parent span is the current span again

        end_dt = time.time()
        latency = end_dt - start_dt
        parent_span.set_attribute('e2e_latency', latency)
    return 'Finished.'


@app.route("/sorting")
def sorting():
    # Create a new span to track some work
    with tracer.start_as_current_span("sorting") as parent_span:
        start_dt = time.time()
        kind = request.args.get('kind')
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        size = int(request.args.get('size'))

        data = generate_data(start=start, end=end, size=size)
        sort_data(data=data, kind=kind)

        # Now the parent span is the current span again
        end_dt = time.time()
        latency = end_dt - start_dt
        parent_span.set_attribute('e2e_latency', latency)
    return 'Request completed.'


def generate_data(start, end, size):
    with tracer.start_as_current_span("generate-data-op") as child_span1:
        child_span1.set_attribute('start_range', start)
        child_span1.set_attribute('end_range', end)
        child_span1.set_attribute('size', size)
        data = np.random.randint(start, end, size=size)
        return data


def sort_data(data, kind):
    with tracer.start_as_current_span("sort-data-op") as child_span2:
        child_span2.set_attribute('kind', kind)
        sorted_data = np.sort(data, axis=0, kind=kind)
        save_data(data=sorted_data, kind=kind)


def save_data(data, kind):
    with tracer.start_as_current_span("save-data-op") as child_span3:
        # child_span3.set_attribute('start_range', start)
        # child_span3.set_attribute('end_range', end)
        server = request.remote_addr
        client = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ['REMOTE_ADDR'])
        # client = '127.0.0.1'
        # Creating a connection cursor
        cursor = mysql.connection.cursor()

        # Executing SQL Statements

        #try:
        #    cursor.execute(''' DROP TABLE sorted_data ''')
        #except Exception as error:
        #    logging.warning("Table does not exist: {}".format(error))

        try:
            cursor.execute(
                ''' CREATE TABLE sorted_data(
                id INT AUTO_INCREMENT PRIMARY KEY, 
                server VARCHAR(255),
                client VARCHAR(255), 
                algorithm VARCHAR(255),
                value INT UNSIGNED) ''')
        except Exception as error:
            logging.fatal("Table is not created: {}".format(error))

        try:
            for value in data:
                cursor.execute(''' INSERT INTO sorted_data(server, client, algorithm, value) VALUES(%s, %s, %s, %s) ''',
                               (server, client, kind, value))
        except Exception as error:
            logging.error("Data is not inserted: {}".format(error))

        # Saving the Actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()


@app.route("/normal_load")
def normal_load():
    hdd = int(request.args.get('hdd'))
    io = int(request.args.get('io'))
    vm = int(request.args.get('vm'))
    cpu = int(request.args.get('cpu'))
    timeout = int(request.args.get('timeout'))

    # Create a new span to track some work
    with tracer.start_as_current_span("parent") as parent_span:
        proc = subprocess.Popen(
            "stress --hdd " + str(hdd) + " --io " + str(io) + " --vm " + str(vm) + " --cpu " + str(
                cpu) + " --timeout " + str(timeout) + "s",
            stdout=subprocess.PIPE,
            shell=True)
        parent_span.set_attribute('hdd', hdd)
        parent_span.set_attribute('io', io)
        parent_span.set_attribute('vm', vm)
        parent_span.set_attribute('cpu', cpu)
        parent_span.set_attribute('timeout', timeout)

    try:
        outs, errs = proc.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        proc.kill()
        abort(500, description="The timeout is expired!")

    if errs:
        abort(500, description=errs.decode('utf-8'))

    return 'Finished'


@app.errorhandler(500)
def server_error(error):
    return jsonify(success=False, message=error.description), 500


# app.run((host="0.0.0.0")
if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)

# curl 'http://127.0.0.1:5000/roll?sides=10&rolls=5'
# curl 'http://127.0.0.1:5000/multispan'
# curl 'http://127.0.0.1:5000/normal_load?hdd=1&io=1&vm=1&cpu=1&timeout=60'
