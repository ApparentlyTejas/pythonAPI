# Travel Destinations

Flask REST API with a browser frontend for tracking travel destinations.

## Setup

```bash
cp .env.example .env
make install
make run
```

Opens at http://localhost:5000.

## Tests

```bash
make test
```

## Endpoints

| Method | Path | Body |
|--------|------|------|
| GET | `/destinations` | |
| GET | `/destinations/<id>` | |
| POST | `/destinations` | `{destination, country, rating}` |
| PUT | `/destinations/<id>` | any subset |
| DELETE | `/destinations/<id>` | |

`rating` is a float 0–5. All three fields required on POST.

Errors return `{"error": "..."}`. Validation errors include a `details` object.

## Structure

```
app.py                 create_app()
config.py              dev/test/prod configs
extensions.py          db instance
models.py
errors.py
routes/destinations.py
templates/index.html
static/
tests/
```

## Env

| Var | Default |
|-----|---------|
| `APP_ENV` | `development` |
| `SECRET_KEY` | `dev` |
| `DATABASE_URL` | `sqlite:///travel.db` |
