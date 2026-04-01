FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY services/ussd_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY services/ussd_service/app.py /app/app.py
CMD ["waitress-serve", "--listen=0.0.0.0:8050", "app:app"]
