FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN opentelemetry-bootstrap --action=install

COPY app.py .

EXPOSE 5002

# Didn't work.
# CMD ["opentelemetry-instrument", "flask", "run", "--host", "0.0.0.0", "--port", "5002", "--debug"]

CMD ["opentelemetry-instrument", "python", "./app.py"]
