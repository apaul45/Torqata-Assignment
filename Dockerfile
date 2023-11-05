FROM python:3.8

RUN pip install 'poetry==1.5.1'

# WORKDIR acts like a cd/mkdir command
WORKDIR /backend

COPY . .

# Project initialization
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "serve"]