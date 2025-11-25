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

-----------------------------
4. Carregar a versão do alembic
docker exec -it backend_app bash
alembic upgrade head


## Para gerar nova versão de banco
docker exec -it backend_app bash
alembic revision --autogenerate -m "nova versão"


<!--

## Requesitos Implmentados

1. ...

## Alterações de Projeto

1. [ADR??](link aqui)

-->
