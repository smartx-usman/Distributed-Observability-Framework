import subprocess
import time
from random import randint

from flask import Flask, request, jsonify, abort
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

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

#app.run((host="0.0.0.0")
# if __name__ == "__main__":
#    from waitress import serve
#    serve(app, host="0.0.0.0", port=5000)

# curl 'http://127.0.0.1:5000/roll?sides=10&rolls=5'
# curl 'http://127.0.0.1:5000/multispan'
# curl 'http://127.0.0.1:5000/normal_load?hdd=1&io=1&vm=1&cpu=1&timeout=60'
