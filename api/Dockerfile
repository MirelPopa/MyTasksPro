FROM python:3.11

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "api.main:fast_api_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
