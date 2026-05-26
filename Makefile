.PHONY: run test install

install:
	uv sync --all-groups

run:
	uv run python app.py

test:
	uv run pytest tests/ -v
