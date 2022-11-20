# KBP
(Named after Kyiv Boryspil Airport)

- [KBP](#kbp)
  - [Run dev environment](#run-dev-environment)
  - [Links](#links)

## Run dev environment
```bash
docker compose up
```

This will run the application in code reload mode, an instance of Postgres, and an instance of minio to emulate s3.

***Do not forget to run migrations***
```bash
alembic upgrade head
```
[Checkout alembic docs](docs/tools.md#alembic)

## Links
* [Database](docs/db_schema.md)
* [Tools](docs/tools.md)