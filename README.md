# Webshop REST API (FastAPI)

A small REST API for a webshop that manages users, shopping baskets and the products in them. Data validation is done with Pydantic and the data is stored in a JSON file.

Built as a university project at ELTE Faculty of Informatics (Python, spring semester 2025/26). Graded 94/100.

## Features

- **Users**: create a user, get one user by ID, list all users.
- **Shopping baskets**: create a basket for an existing user (one basket per user, with an auto-incremented basket ID).
- **Basket items**: add, update and delete products in a user's basket, list the basket's contents, and get the basket total (sum of price × quantity, rounded to 2 decimals).
- **Validation**: Pydantic v2 models (`User`, `Basket`, `Item`) reject negative IDs, prices and quantities and invalid e-mail addresses (`EmailStr`). Invalid requests return `422`.
- **Error handling**: errors from the data layer (`ValueError`) become HTTP errors: `400` for duplicate users or baskets, `404` when a user, basket or item is missing.
- **Backup and restore**: `/save` and `/reload` copy a JSON data file to another file name inside `data/`.
- **Interactive docs**: Swagger UI and ReDoc are generated automatically by FastAPI.

## Endpoints

| Method | Path | Parameters | Description |
|--------|------|------------|-------------|
| GET    | `/` | none | Welcome message |
| POST   | `/adduser` | body: `User` | Create a user |
| GET    | `/user` | `userid` | Get a user |
| GET    | `/users` | none | List all users |
| POST   | `/addshoppingbag` | `userid` | Create a basket for a user |
| POST   | `/additem` | `userid`, body: `Item` | Add a product to the user's basket |
| PUT    | `/updateitem` | `userid`, `itemid`, body: `Item` | Replace a product in the basket |
| DELETE | `/deleteitem` | `userid`, `itemid` | Remove a product from the basket |
| GET    | `/shoppingbag` | `userid` | List the products in the basket |
| GET    | `/getusertotal` | `userid` | Total price of the basket |
| POST   | `/save` | `source`, `dest` | Copy a data file (backup) |
| POST   | `/reload` | `dest`, `source` | Copy a data file back (restore) |

## Tech stack

- Python 3.9+
- FastAPI, Uvicorn
- Pydantic v2 (with `email-validator` for `EmailStr`)
- JSON file storage (`data/data.json`)

## How to run

```bash
git clone https://github.com/toroktomi/webshop-fastapi.git
cd webshop-fastapi
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Run the `uvicorn` command from the project root so that the `schemas`, `routers` and `data` packages can be imported.

- API: http://127.0.0.1:8000
- Swagger UI (interactive docs): http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

`data/data.json` contains sample users and baskets. The API writes to this file, so make a copy first (or use `/save`) if you want to keep the original data.

## Project structure

```
main.py              FastAPI app, includes the router
routers/routes.py    All API endpoints
schemas/schema.py    Pydantic models: User, Basket, Item
data/filereader.py   Read operations on the JSON store
data/filehandler.py  Write operations on the JSON store
data/data.json       Sample data
```

## What I learned / key challenges

- Designing request and response models with Pydantic v2 (`Field` constraints, `field_validator`, `EmailStr`) so that FastAPI rejects invalid input before it reaches the business logic.
- Mapping domain errors (`ValueError` from the storage layer) to the right HTTP status codes (`201`, `400`, `404`, `500`).
- Splitting the code into layers (routing, schemas, storage) with `APIRouter`, and keeping a JSON file consistent across read-modify-write operations.

## Author

Török Tamás
