# MATA62 - Grupo 2 - Backend

## Introdução

Este repositório contém a implementação da arquitetura projetada pelo Grupo 2 e implementada pelo Grupo 1.

## Instruções de Uso

1. Criar um ambiente virtual e ativar.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar as bibliotecas necessárias.

```bash
pip install --editable .
```

3. Iniciar container
```bash
docker-compose up --detach --build
```

3. Executar o código.

```bash
fastapi dev src/main.py
```
-----------------------------
Para rodar app
docker compose up
alembic revision --autogenerate -m "nova versão"


Para gerar nova versão alembic
docker exec -it backend_app bash

<!--

## Requesitos Implmentados

1. ...

## Alterações de Projeto

1. [ADR??](link aqui)

-->
