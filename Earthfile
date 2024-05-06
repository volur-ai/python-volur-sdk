VERSION 0.8

# install-base configures the base image for the project
# - creates a virtual environment for Poetry
# - installs Poetry from `poetry/requirements.txt`
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
            --quiet \
            --requirement requirements.txt && \
        rm -rf requirements.txt

# generate-requirements generates the `poetry/requirements.txt` file
# - uses pip-compile to generate a list of dependencies from `poetry/requirements.in
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
        requirements.in
    SAVE ARTIFACT /srv/workspace/requirements.txt AS LOCAL poetry/requirements.txt


# configure installs the library dependencies
configure:
    FROM +install-base
    COPY poetry.toml pyproject.toml poetry.lock ./
    COPY mkdocs.yml ./
    RUN poetry install --sync --no-root
    COPY --dir src gen tests examples scripts docs .
    RUN poetry install --sync

# upgrade-dependencies upgrades the library dependencies to their latest compatible version
# using `poetry-plugin-upgrade`
upgrade-dependencies:
    FROM +configure
    RUN poetry upgrade --latest
    SAVE ARTIFACT /srv/workspace/pyproject.toml AS LOCAL pyproject.toml
    SAVE ARTIFACT /srv/workspace/poetry.lock AS LOCAL poetry.lock

# update-dependencies updates the library dependencies to their latest compatible version
# according to the constraints in `pyproject.toml`
update-dependencies:
    FROM +configure
    RUN poetry lock
    SAVE ARTIFACT /srv/workspace/poetry.lock AS LOCAL poetry.lock

# lock-dependencies locks the library dependencies to their compatible version
lock-dependencies:
    FROM +configure
    RUN poetry lock --no-update
    SAVE ARTIFACT /srv/workspace/poetry.lock AS LOCAL poetry.lock

# generate generates code from the APIs declarations
generate:
    BUILD github.com/volur-ai/apis:main+generate-python

# fix fixes all auto-fixable formatting and linting issues
fix:
    FROM +configure
    RUN poetry run ruff format src tests examples scripts && \
        poetry run ruff check --fix --unsafe-fixes src tests examples scripts
    SAVE ARTIFACT /srv/workspace/src AS LOCAL src
    SAVE ARTIFACT /srv/workspace/tests AS LOCAL tests
    SAVE ARTIFACT /srv/workspace/examples AS LOCAL examples
    SAVE ARTIFACT /srv/workspace/scripts AS LOCAL scripts

# validate validates the library (project configuration, linting and static
# type checking)
validate:
    FROM +configure
    COPY *.ipynb .
    RUN poetry check --lock && \
        poetry run ruff format --check src tests scripts *.ipynb && \
        poetry run ruff check src tests scripts *.ipynb && \
        poetry run mypy src tests scripts

# test runs the library unit tests
test:
    FROM +configure
    RUN poetry run pytest tests
    SAVE ARTIFACT /srv/workspace/.coverage AS LOCAL .coverage
    SAVE ARTIFACT /srv/workspace/htmlcov AS LOCAL htmlcov

# build-docs builds the documentation using mkdocs
build-docs:
    FROM +configure
    RUN poetry run mkdocs build
    SAVE ARTIFACT /srv/workspace/site AS LOCAL site

# ci runs the CI pipeline (linting, static type checking, unit tests, documentation generation) locally
ci:
    BUILD +validate
    BUILD +test
    BUILD +build-docs
