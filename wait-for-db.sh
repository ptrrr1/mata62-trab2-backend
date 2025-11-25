#!/bin/sh
DB_HOST=db
DB_PORT=3306
DB_ROOT=root
DB_ROOT_PASS=root_password
DB_NAME=soccer_quiz

echo "⏳ Aguardando MySQL subir..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "✅ MySQL está online!"

# Cria o banco se não existir usando root
mysql -h $DB_HOST -u $DB_ROOT -p$DB_ROOT_PASS -e "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"

echo "🚀 Rodando migrações Alembic..."
alembic upgrade head

echo "🚀 Iniciando FastAPI..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug