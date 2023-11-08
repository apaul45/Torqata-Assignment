FROM python:3.8

ENV IS_DEV=true

# WORKDIR acts like a cd/mkdir command
WORKDIR /backend

# Cache requirements 
COPY poetry.lock pyproject.toml /backend/

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1 
ENV PATH="/root/.local/bin:$PATH"

# Allow for caching by running poetry install without needing project present
# poetry install by default requires project present, which causes layer changes in docker whenever files change
RUN poetry install --no-root --no-directory 

COPY . .

# Project initialization
RUN poetry install --no-interaction --no-ansi $(test "$IS_DEV" == "false" && echo "--no-dev")

CMD ["poetry", "run", "serve"]