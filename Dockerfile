FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir .

CMD []