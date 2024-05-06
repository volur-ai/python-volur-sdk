default:
    just list

configure:
    poetry install --sync --no-root

upgrade-dependencies:
    poetry upgrade --latest

lock-dependencies:
    poetry lock --no-update

fix:
    poetry run ruff format src tests && \
    poetry run ruff check --fix --unsafe-fixes src tests

validate:
    poetry check --lock && \
    poetry run ruff format --check src tests && \
    poetry run ruff check src tests && \
    poetry run mypy src tests

test:
    poetry run pytest tests

ci: validate test