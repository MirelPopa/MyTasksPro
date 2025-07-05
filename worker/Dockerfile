FROM python:3.11

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["celery", "-A", "worker.main.celery_app", "worker"]
