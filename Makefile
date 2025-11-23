SHELL=/bin/bash

revision:
	source .env.local && alembic revision --autogenerate -m "$(msg)"

upgrade:
	source .env.local && alembic upgrade head