# Nodes
Check the challenge in the `docs` folder.

## Requirements
The project uses sqlite, so the only requirement is:

- `python3`

## Setup
- `$ python3 -m venv .venv`
- `$ source .venv/bin/activate`
- `$ pip install -r requirements-dev.txt`

## Type checking
- `$ mypy`

## Formatting
- `$ black .`

## Running the application
- `$ flask --app nodes run --debug`

Go to the browser and try a sample API call like:
`http://127.0.0.1:5000/nodes/5/children?language=italian`

## Test
- `$ pytest`