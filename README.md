# Nodes

Minimal Flask API to explore a nested set model.

Check the challenge in the `docs` folder.

![Test](https://github.com/andreafspeziale/nodes/actions/workflows/test.yml/badge.svg)
![License: MIT](https://img.shields.io/github/license/andreafspeziale/nodes.svg)


## Requirements

The project uses sqlite, so the only requirement is:

- `python3`

## Quickstart

```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements-dev.txt -r requirements.txt
$ pre-commit install
$ flask --app nodes run --debug
```
>Go to the browser and try a sample API call like:
`http://127.0.0.1:5000/api/nodes/5/children?language=italian`

### Development

```sh
$ mypy               # type check
$ black .            # formatting
$ pylint nodes tests #linting
$ pytest             # tests
```

## Stay in touch

- Author - [Andrea Francesco Speziale](https://twitter.com/andreafspeziale)

## License

nodes [MIT licensed](LICENSE).

