# NatMovies — Movies Project

NatMovies is a full-stack application to browse, filter, and manage movies. It exposes a Django REST API and an Angular frontend. Users can list, search, filter by genre and rating, view details, and create/update/delete movies.

Documentation: https://natmovies.readthedocs.io/en/latest/index.html

## Features
- Django REST API for movies CRUD
- Angular UI with filters (genre, rating), pagination, and details
- Seed command to populate initial data
- Unit tests for backend API

## Architecture
- Backend (Django/DRF): [backend](/backend)
  - Settings: [backend/backend/settings.py](/backend/backend/settings.py)
  - URLs: [backend/movies/urls.py](/backend/movies/urls.py)
  - Model: [`movies.models.Movie`](/backend/movies/models.py)
  - Seed command: [`movies.management.commands.seed_data.Command`](/backend/movies/management/commands/seed_data.py)
  - Tests: [backend/movies/tests.py](/backend/movies/tests.py)
- Frontend (Angular): [movies-frontend](/movies-frontend)
  - Movies component: [`app.components.movies.Movies`](/movies-frontend/src/app/components/movies/movies.ts)

## Requirements
- Python 3.10+
- Node.js 18+ and npm
- Angular CLI
- Docker (optional)

## Backend — Setup and Run
1) Create and activate a virtualenv
- Windows:
  ```sh
  python -m venv .venv && .venv\Scripts\activate
  ```
- Linux/macOS:
  ```sh
  python -m venv .venv && source .venv/bin/activate
  ```

2) Install dependencies
```sh
pip install -r backend/requirements.txt
```

3) Migrate database
```sh
cd backend
python manage.py migrate
```

4) Seed initial data (superuser + movies)
```sh
python manage.py seed_data
```

5) Run the server
```sh
python manage.py runserver
# API: http://localhost:8000/
```

API endpoints (via DRF router):
- `GET/POST /movies/`
- `GET/PUT/PATCH/DELETE /movies/{id}/`

## Frontend — Setup and Run
```sh
cd movies-frontend
npm ci
ng serve
# Open http://localhost:4200/
```

## Docker
Backend (Django):
```sh
cd backend
docker build -t natmovies-backend .
docker run --rm -p 8000:8000 natmovies-backend
# Container runs migrations then serves at 0.0.0.0:8000
```

Frontend (Angular dev server):
```sh
cd movies-frontend
docker build -t natmovies-frontend .
docker run --rm -p 4200:4200 natmovies-frontend
# Open http://localhost:4200/
```

## Tests
Backend:
```sh
cd backend
python manage.py test
```

Frontend (Vitest via Angular CLI):
```sh
cd movies-frontend
ng test
```

## Docs
- Online: https://natmovies.readthedocs.io/en/latest/index.html
- Source: [docs/source/conf.py](/docs/source/conf.py), build helpers: [docs/Makefile](/docs/Makefile/), [docs/make.bat](/docs/make.bat), config: [.readthedocs.yaml](/.readthedocs.yaml)
- Build locally:
  ```sh
  cd docs
  make html
  # Open build/index.html under docs/build/
  ```
