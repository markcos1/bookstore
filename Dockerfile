# Ajuste a versão do Python (ex: 3.11-slim ou 3.12-slim) conforme o seu pyproject.toml
FROM python:3.14-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Adiciona o Poetry e o ambiente virtual (.venv) ao PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry pelo instalador oficial atual (substitui o antigo get-poetry.py)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copia os arquivos de dependências do Poetry
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Instala as dependências do projeto (sem instalar o pacote raiz caso não seja uma lib)
RUN poetry install --no-root

WORKDIR /app
COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

