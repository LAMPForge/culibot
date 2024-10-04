# Server

## Getting started

```bash
# Run these commands in this directory (./server)
#
# Create a .env file and edit it
cp .env.example .env

# Start PostgreSQL
docker compose up -d

# Install dependencies, enter the poetry shell
poetry install
poetry shell
```

## Create a database migration

Modify the model in ```culi.model```, then run

```bash
alembic revision --autogenerate -m "[description]"
```

and a migration will be generated for you.

## Design

### How a module is structured

| culi/your_module/ | Explanation & Usage |
|-------------------|---------------------|
| endpoints.py      | FastAPI `router` for the module. Mounted and routed in `culi.api`. Endpoint functions should be in charge of validation and authentication, but business logic should be contained within `service.py` |
| schemas.py        | Pydantic schemas for request/response and data validation. Resources should have schemas for their applicable CRUD operations named `<Resource>(Read\|Create\|Update\|Delete)` |
| service.py        | Module containing all the business logic. Essentially the non-public API for the resource/service which its own API utilizes along with any other services. |
| exceptions.py     | Any local exceptions. |
| ***               | resources/services are the same. So extend it as needed. |