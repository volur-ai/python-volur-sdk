FROM docker.io/library/python:3.11.9@sha256:db07fba48daaf1c68c03676aadc73866414d25b4c278029f9873c784517613bf AS python
FROM mcr.microsoft.com/azure-functions/python:4-python3.11-slim@sha256:019a716b801ada5640cd27d12e9999fa3a72997331aa2db0ab3b8ad95b4148d7 AS azure-functions

FROM python AS requirements

WORKDIR /srv/workspace

ENV VENV_PATH="/opt/poetry"
ENV PATH="${VENV_PATH}/bin:$PATH"

COPY poetry/requirements.txt requirements.txt

RUN python -m venv $VENV_PATH && \
    $VENV_PATH/bin/pip install \
        --no-cache-dir \
        --require-hashes  \
        --use-pep517 \
        --requirement requirements.txt && \
    rm -rf requirements.txt

COPY pyproject.toml poetry.lock ./
RUN poetry export --output=requirements.txt --without-hashes

FROM azure-functions AS deployment

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN apt-get update && \
    apt-get install --yes --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=requirements /srv/workspace/requirements.txt .

RUN --mount=type=secret,id=GH_TOKEN \
    git config \
        --global \
        --add url."https://oauth:$(cat /run/secrets/GH_TOKEN)@github.com/volur-ai".insteadOf "https://github.com/volur-ai" && \
    pip install \
        --no-cache-dir \
        --requirement requirements.txt && \
    rm -rf requirements.txt

COPY host.json /home/site/wwwroot/
COPY function_app.py /home/site/wwwroot/
