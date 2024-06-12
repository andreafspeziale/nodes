FROM python:3.10-alpine as build

WORKDIR /usr/nodes-app
RUN python3 -m venv .venv
ENV PATH="/usr/nodes-app/.venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

FROM python:3.10-alpine as runner

EXPOSE 8000

RUN addgroup python && adduser -G python -D python

RUN mkdir /usr/nodes-app && chown python:python /usr/nodes-app
WORKDIR /usr/nodes-app

COPY --chown=python:python --from=build /usr/nodes-app/.venv ./.venv
COPY --chown=python:python nodes/ ./nodes
COPY --chown=python:python setup.py .

USER python

ENV PATH="/usr/nodes-app/.venv/bin:$PATH"
CMD ["gunicorn", "--bind", "0.0.0.0", "--access-logfile", "-", "nodes:create_app()"]
