# FastApi sample

Example of a python microservices using FastApi framework

## Requirements

- Python 3
- Virtual env
- VSCode or an other IDE
  - [Autopep8 extension](https://marketplace.visualstudio.com/items?itemName=himanoa.Python-autopep8)

## Features

- [x] Service documentation (Open api)
- [x] Logger
- [x] Multiple environments with dotenv
- [x] Docker
- [x] Mongo connector with Motor
- [x] Authentication check (Test with keycloak)
- [x] Authentication roles check (Test with keycloak)
- [ ] Gitlab CI
- [x] Unit test with pytest
- [x] Cache
- [ ] Kafka connector

## Start

- Run `./make.sh` to build the virtual env
- Copy and set `.env-sample` to `.env`, edit variables
- Run `python main.py` or use a launcher in VScode for example
- Access to http://127.0.0.1:8080/
- Access to http://127.0.0.1:8080/docs for swagger
- Access to http://127.0.0.1:8080/redoc for Redoc

## Tests

- Write tests in `tests` folder
- File pattern should be `*_test.py`
- Run with the command `pytest`

## Helpfull links

- [Python virtual env](https://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.htmls)
- [Python 3](https://www.python.org/)
- [Starlette](https://www.starlette.io/websockets/)
- [FastAPI](https://fastapi.tiangolo.com//)
