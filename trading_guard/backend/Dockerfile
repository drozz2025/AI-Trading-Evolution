FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml ./
COPY app ./app

RUN pip install --no-cache-dir "fastapi>=0.116,<1" "uvicorn[standard]>=0.35,<1"

EXPOSE 10000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
