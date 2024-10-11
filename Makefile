.PHONY: run
run:
	uvicorn main:app --reload --app-dir ./simple-chat-app/.

.PHONY: lint
lint:
	isort .
	black .
	flake8 .
	mypy .

.PHONY: migrate
migrate:
	alembic upgrade head
