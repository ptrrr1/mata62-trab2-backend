#!/bin/sh
DB_HOST=db
DB_PORT=3306

echo "⏳ Aguardando MySQL subir..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "⏳ Aguardando mais 10 segundos para MySQL estar totalmente pronto..."
sleep 10

echo "✅ MySQL está online!"

echo "🚀 Iniciando FastAPI (tabelas serão criadas automaticamente)..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug