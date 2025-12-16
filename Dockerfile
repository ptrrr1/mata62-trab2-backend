FROM python:3.10


WORKDIR /app

COPY . .
RUN apt-get update && apt-get install -y netcat-traditional
RUN pip install --no-cache-dir .


CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
