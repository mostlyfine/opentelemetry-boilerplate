# Twitter Clone with OpenTelemetry

A Flask-based Twitter clone application with OpenTelemetry distributed tracing and Locust load testing support.

## Features

- User registration and login
- Tweet posting and viewing
- Follow/follower functionality
- Like functionality
- Search functionality
- Trending tweets

## Technology Stack

- **Backend**: Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Web Server**: nginx
- **Monitoring**: OpenTelemetry
- **Load Testing**: Locust

## Getting Started

### Prerequisites

OpenTelemetry Collector must be running:

```bash
# From the main directory
docker-compose up -d opentelemetry-collector grafana tempo mimir loki
```

### Application Startup

```bash
OTEL_APP=twitter docker-compose up -d
```

### Access

- **Application**: http://localhost
- **Load Testing (Locust)**: http://localhost:8089

### Test Login Credentials

The application starts with a pre-populated SQLite database. You can use the following test accounts or register a new user:

- **Email**: `user0001@example.com` - `user0100@example.com`
- **Password**: `password123`

Alternatively, register a new account using any email format and password of your choice.

## OpenTelemetry Configuration

### Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://opentelemetry-collector:4318` | OTLP export destination |
| `OTEL_RESOURCE_ATTRIBUTES` | `service.name=twitter-app,service.namespace=twitter` | Service information |

### Traced Components

- HTTP requests (Flask)
- SQL queries (SQLAlchemy)
- Log output

## Load Testing

Use Locust for application performance testing:

```bash
# Access Locust UI
open http://localhost:8089
```

### Test Scenarios

- User registration
- Login
- Tweet posting
- Timeline viewing
- Follow/unfollow operations

## Development

### Local Development Environment

```bash
cd twitter
docker-compose build
docker-compose up
```

### Development with Auto-reload

```bash
cd twitter
# Build the image
docker-compose build

# Run in development mode with volume mounting for live reload
docker-compose up
```

### Database Initialization

SQLite database and tables are automatically created on first application startup.

### Database Persistence

The SQLite database is mounted as a volume to persist data between container restarts:

```yaml
volumes:
  - ./app/twitter_clone.db:/app/instance/twitter_clone.db
```

This ensures that:
- User accounts and tweets are preserved when containers restart
- Database changes made during development are persistent
- You can backup/restore the database by copying the `app/twitter_clone.db` file

## Troubleshooting

### No Traces Generated

1. Verify OpenTelemetry Collector is running
2. Check environment variables are correctly set
3. Check container logs for error messages

```bash
docker-compose logs app
```

### Database Errors

For SQLite file permission issues:

```bash
chmod 666 app/twitter_clone.db
```

### Container Management

```bash
# Stop all services
docker-compose down

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# View logs for specific service
docker-compose logs -f app

# If containers fail to start, remove and recreate
docker-compose down
docker-compose rm -f
docker-compose build --no-cache
docker-compose up -d
```

## Architecture

```
nginx:80 → twitter-app:5000 → SQLite
     ↓
OpenTelemetry Collector:4318
     ↓
Tempo (traces) + Loki (logs) + Mimir (metrics)
```
