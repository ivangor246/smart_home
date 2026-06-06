.PHONY: dev


dev:
	poetry run uvicorn app.main:create_app \
	--factory --reload --host 127.0.0.1 --port 8000
