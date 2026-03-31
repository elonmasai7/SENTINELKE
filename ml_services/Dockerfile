FROM python:3.12-slim

WORKDIR /app
COPY ml_services/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ml_services /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
