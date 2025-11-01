FROM python:3.10-slim AS builder

WORKDIR /app
COPY app_requirements.txt .
RUN pip install --no-cache-dir --target=/app/libs -r app_requirements.txt
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /app/libs /usr/local/lib/python3.10/site-packages
COPY app.py .
COPY templates/ templates/

EXPOSE 5000

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]]