import os
import requests
import logging
from random import randint
from flask import Flask, jsonify

import pyroscope

# OpenTelemetry
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from pyroscope.otel import PyroscopeSpanProcessor
from opentelemetry import metrics

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
provider.add_span_processor(PyroscopeSpanProcessor())

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
app.json.ensure_ascii = False
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pyroscope.configure(
    application_name="sample-app",
    server_address=os.getenv("PYROSCOPE_SERVER_ADDRESS"),
    enable_logging=True,
    tags={
        "region": f'{os.getenv("REGION", "tokyo")}',
    }
)

meter = metrics.get_meter(__name__)
dice_count = meter.create_gauge("dice_count")


@app.route("/api/rolldice")
def roll_dice():
    dice = randint(0, 6)
    logger.info("rolling the dice: %d", dice)
    dice_count.set(dice)                  # set custom metrics

    with pyroscope.tag_wrapper({"fibonacci": f'dice:{dice}'}):
        fibonacci(dice)
    7 / dice                              # generate error
    return jsonify({"dice": dice})


@app.route("/api/weather/")
@app.route("/api/weather/<int:area>")
def weather(area=130000):
    jma_url = f'https://www.jma.go.jp/bosai/forecast/data/forecast/{area}.json'
    jma_json = requests.get(jma_url).json()
    logger.info(jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0])
    return jsonify(jma_json)


def fibonacci(n):
    if n <= 1:
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
