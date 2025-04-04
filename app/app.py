import os
import requests
import logging
from random import randint
from flask import Flask, jsonify

import pyroscope
from opentelemetry import metrics

app = Flask(__name__)
app.json.ensure_ascii = False
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pyroscope.configure(
    application_name="sample-app",
    server_address=os.getenv("PYROSCOPE_SERVER_ADDRESS"),
    enable_logging=True,
)

meter = metrics.get_meter(__name__)
dice_count = meter.create_gauge("dice_count")


@app.route("/api/rolldice")
def roll_dice():
    result = randint(0, 6)
    logger.info("rolling the dice: %d", result)
    dice_count.set(result)                      # set custom metrics
    7 / result                                  # generate error

    with pyroscope.tag_wrapper({"function": "fibonacci"}):
        fibonacci(result)

    return jsonify({"result": result})


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
