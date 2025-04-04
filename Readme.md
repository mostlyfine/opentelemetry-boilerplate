# Local LGTM Stack and OpentelemetryCollector Test Environment

## Overview

This project provides an easy way to launch and test the Grafana LGTM (Loki, Grafana, Tempo, Mimir and OpenTelemetryCollector) stack in your local environment.
It uses `docker-compose` to start the main components of the LGTM stack (and related tools) together, allowing you to quickly try out log, trace, and metric collection and visualization.

## Objectives

* To easily experiment with the integration of Grafana LGTM stack components (Loki, Grafana, Tempo, Mimir).
* To safely test configurations and queries for log (Loki), trace (Tempo), and metric (Mimir) collection and visualization locally (LogQL, TraceQL, PromQL).
* To simplify learning and demonstration of observability setups.
* You can test the collection of traces, metrics, and logs using OpenTelemetry.

## Key Features

* One-command startup/shutdown of the LGTM stack using Docker Compose.
* Setup of main components: Grafana, Loki, Tempo, Mimir.
* Pre-configured data sources (Loki, Tempo, Mimir) in Grafana.

## Getting Started

### Prerequisites

Ensure you have the following software installed on your local machine:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/) (Usually included with Docker Desktop)

### Installation and Startup

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/mostlyfine/opentelemetry.git
    cd opentelemetry
    ```

2.  **Start the Docker containers:**
    ```bash
    docker-compose build
    docker-compose up -d
    ```
    This will start the required containers in the background. The initial startup might take some time to download the necessary images.

3.  **Check container status  (Optional):**
    ```bash
    docker-compose ps
    ```

4.  **Check container logs  (Optional):**
    ```bash
    docker-compose logs -f opentelemetry-collector
    ```

### Accessible Endpoints

Once the containers are running, you can access the following endpoints:

* **Application:** [http://localhost/](http://localhost) (Sample application for testing)
* **Grafana:** [http://localhost:3000](http://localhost:3000)


### Stopping the Stack

To stop the stack, run the following command in the repository's root directory:

```bash
docker-compose down
```
