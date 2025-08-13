FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap --action=install

COPY . .

EXPOSE 5000

ENV FLASK_APP=main.py
CMD ["opentelemetry-instrument", "flask", "run", "--host=0.0.0.0", "-p", "5000"]
