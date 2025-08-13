# Local LGTM Stack with OpenTelemetry Test Environment

## Overview

This project provides an easy way to launch and test the Grafana LGTM (Loki, Grafana, Tempo, Mimir, Pyroscope) stack with OpenTelemetry Collector in your local environment.
It uses `docker-compose` with modular include files to start the main components of the LGTM stack and related tools together, allowing you to quickly try out log, trace, and metric collection and visualization.

## Objectives

* To easily experiment with the integration of Grafana LGTM stack components (Loki, Grafana, Tempo, Mimir, Pyroscope).
* To safely test configurations and queries for log (Loki), trace (Tempo), metric (Mimir), and profiling (Pyroscope) collection and visualization locally (LogQL, TraceQL, PromQL).
* To simplify learning and demonstration of observability setups.
* You can test the collection of traces, metrics, and logs using OpenTelemetry.

## Key Features

* One-command startup/shutdown of the LGTM stack using Docker Compose with modular configuration.
* Setup of main components: Grafana, Loki, Tempo, Mimir, Pyroscope, OpenTelemetry Collector.
* Pre-configured data sources (Loki, Tempo, Mimir, Pyroscope) in Grafana.
* Multiple example applications for testing OpenTelemetry integration:
  - Python app with log output and Pyroscope profiling
  - Jaeger example with Locust load testing capabilities
  - Twitter clone app with social media features and load testing
* Environment variable support for switching between different applications (OTEL_APP).

## Getting Started

### Prerequisites

Ensure you have the following software installed on your local machine:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/) (Usually included with Docker Desktop)

### Installation and Startup

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/mostlyfine/opentelemetry-boilerplate.git
    cd opentelemetry-boilerplate
    ```

2.  **Start the Docker containers:**
    ```bash
    docker-compose up -d
    ```
    This will start all the required containers in the background. The initial startup might take some time to download the necessary images.

    **To use the Jaeger example instead of the default Python app:**
    ```bash
    OTEL_APP=jeager-example docker-compose up -d
    ```

    **To use the Twitter clone app:**
    ```bash
    OTEL_APP=twitter docker-compose up -d
    ```

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

* **Grafana:** [http://localhost:3000](http://localhost:3000) (Observability dashboard)
* **Sample Applications:**
  - **Python App (default):** [http://localhost](http://localhost) (Flask application with OpenTelemetry, includes log output and Pyroscope profiling)
  - **Jaeger Example:** [http://localhost](http://localhost) (when `OTEL_APP=jeager-example`, includes Locust load testing capabilities)
  - **Twitter Clone App:** [http://localhost](http://localhost) (when `OTEL_APP=twitter`, social media app with OpenTelemetry tracing and load testing)
    - **Login credentials:** user[0001-0100]@example.com / password123


### Load Testing with Jaeger Example

When using the Jaeger example (`OTEL_APP=jeager-example`), you can perform load testing using Locust:

1. **Start the Jaeger example:**
   ```bash
   OTEL_APP=jeager-example docker-compose up -d
   ```

2. **Access Locust web UI:**
   Open [http://localhost:8089](http://localhost:8089) in your browser

3. **Configure load test:**
   - **Number of users:** Set the total number of concurrent users
   - **Spawn rate:** Set how many users to start per second
   - **Host:** Use `http://nginx` (the internal service name)

4. **Start load test:**
   Click "Start swarming" to begin the load test and monitor the results in real-time

The load test will generate traffic to various endpoints with different customer IDs, creating traces and metrics that you can observe in Grafana.

### Load Testing with Twitter Clone App

When using the Twitter clone app (`OTEL_APP=twitter`), you can perform load testing using Locust:

1. **Start the Twitter clone app:**
   ```bash
   OTEL_APP=twitter docker-compose up -d
   ```

2. **Access Locust web UI:**
   Open [http://localhost:8089](http://localhost:8089) in your browser

3. **Configure load test:**
   - **Number of users:** Set the total number of concurrent users
   - **Spawn rate:** Set how many users to start per second
   - **Host:** Use `http://nginx` (the internal service name)

4. **Start load test:**
   Click "Start swarming" to begin the load test and monitor the results in real-time

The load test will simulate various Twitter-like activities including user interactions, posting tweets, and browsing timelines, creating comprehensive traces and metrics for observability testing.

### Stopping the Stack

To stop the stack, run the following command in the repository's root directory:

```bash
docker-compose down
```

## License

This project is licensed under the MIT License.
