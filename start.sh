#!/bin/sh

echo "🚀 Iniciando aplicação no Render..."

# O Render injeta a variável $PORT automaticamente.
# Se $PORT não existir (localmente), usa 8000.
PORTA_ATUAL=${PORT:-8000}

echo "🔌 Rodando na porta: $PORTA_ATUAL"

# Inicia o Uvicorn apontando para a porta correta
exec uvicorn src.main:app --host 0.0.0.0 --port $PORTA_ATUAL