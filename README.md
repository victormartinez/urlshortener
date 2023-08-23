# URL Shorten API

This is a project responsible for shortening URLs.

## Requirements

- Python (~3.10) + FastAPI 🐍
- Docker + docker-compose 🐋

## Architectural Decision

A report is provided at [./docs](./docs) directory.

## Getting Started

1. Clone the repo
    ```
    git clone git@github.com:victormartinez/urlshorten.git
    ```

2. Create a `.env` file from `env.sample`

3. Install the dependencies
    ```
    cd urlshorten/
    poetry install
    ```

4. Split the terminal and execute the commands below:
    ```
    # first terminal
    make up

    # second terminal
    make run
    ```

- Application: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- API Doc: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- PGAdmin (user: `dev@dev.com` pass: `postgres`): [http://127.0.0.1:8080](http://127.0.0.1:8080)

### Main Commands

Makefile makes available most used commands.

```sh
make help
```

```sh
make format
```

```sh
make coverage
```

```sh
make unit-test
```

```sh
make integration-test
```
