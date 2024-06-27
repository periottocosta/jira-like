# Jira like API

Django rest API integrated with Postgres and Docker.
​

- [Config](#config)
- [Run the application](#running)
- [Tests](#tests)
- [Documentation](#documentation)
  ​

## Config

Create a `.env` file with this content:

```
POSTGRES_DB=myproject_db
POSTGRES_USER=myproject_user
POSTGRES_PASSWORD=myproject_password
```

## Running

Has two options to run this project: docker or manually

### Running with docker

- Install Docker compose following this [documentation](https://docs.docker.com/compose/install/)
  Run:

```
docker-compose up
```

### Running local

- Install pyenv following this [documentation](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
- Install Python with pyenv
  ```
  pyenv install 3.9
  ```
- Install poetry:
  ```
  curl -sSL https://install.python-poetry.org | python3 -
  ```
- Set poetry version running :
  ```
  poetry self update 1.1.12
  ```
- Create virtual env:
  ```
  poetry shell
  ```
- Install the dependencies:

  ```
  poetry install
  ```

- Then start API running:
  ```
  make run-server
  ```

## Tests

Test only can be executed locally, so you need to install dependencies then run:

```
make coverage-test
```

## Documentation

Swagger doc can be access from the URL:

```
http://localhost:8000/redoc
or
http://localhost:8000/swagger
```
