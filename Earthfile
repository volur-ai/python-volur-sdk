VERSION 0.7

# configure base image with poetry and all required
# tooling for development
install-base:
    FROM DOCKERFILE --target=python .
    WORKDIR /srv/workspace
    ENV VENV_PATH="/opt/poetry"
    ENV PATH="${VENV_PATH}/bin:$PATH"
    COPY poetry/requirements.txt .
    RUN python -m venv $VENV_PATH && \
        ${VENV_PATH}/bin/pip install \
          --no-cache-dir \
          --require-hashes \
          --use-pep517 \
          --requirement requirements.txt && \
        rm -rf requirements.txt

# a boostrap target to generate a requirements.txt for poetry
generate-requirements:
    FROM +install-base
    COPY poetry/requirements.in .
    RUN pip-compile \
		  --allow-unsafe \
		  --annotate \
		  --generate-hashes \
		  --output-file requirements.txt \
		  --rebuild \
		  --resolver backtracking \
		  --verbose \
		  requirements.in
	SAVE ARTIFACT /srv/workspace/requirements.txt AS LOCAL poetry/requirements.txt

# run this to configure the development environment
configure:
    FROM +install-base
    COPY poetry.toml pyproject.toml poetry.lock ./
    RUN poetry install --sync --no-root
    COPY --dir src gen tests .

# run this if you want to upgrade the dependencies
upgrade-dependencies:
    FROM +configure
    RUN poetry upgrade --latest
    SAVE ARTIFACT /srv/workspace/pyproject.toml AS LOCAL pyproject.toml
    SAVE ARTIFACT /srv/workspace/poetry.lock AS LOCAL poetry.lock

# run this if you want to re-lock the dependencies
lock-dependencies:
    FROM +configure
    RUN poetry lock --no-update
    SAVE ARTIFACT /srv/workspace/poetry.lock AS LOCAL poetry.lock

# generate Python code from `apis` repo `protobuf`s
generate:
    BUILD github.com/volur-ai/apis:main+generate-python

# fix auto-fixable issues
fix:
    FROM +configure
    RUN poetry run ruff format src tests && \
        poetry run ruff check --fix --unsafe-fixes src tests
    SAVE ARTIFACT /srv/workspace/src AS LOCAL src
    SAVE ARTIFACT /srv/workspace/tests AS LOCAL tests

# run static validation
validate:
    FROM +configure
    COPY *.ipynb .
    RUN poetry check --lock && \
        poetry run ruff format --check src tests *.ipynb && \
        poetry run ruff check src tests *.ipynb && \
        poetry run mypy src tests

test:
    FROM +configure
    RUN poetry install
    RUN poetry run pytest tests

# Run CI locally
ci:
    BUILD +validate
    BUILD +test

# Build the docs
build-docs:
    FROM +configure
    COPY mkdocs.yml .
    COPY --dir docs scripts .
    RUN poetry run mkdocs build
