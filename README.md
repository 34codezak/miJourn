# miJourn Container Deployment

This repository now includes Docker assets for running the Django application in a container that matches the expected Heroku environment. The Docker image installs Python dependencies from [`Journal/requirements.txt`](Journal/requirements.txt), collects static files with WhiteNoise, and serves the project using Gunicorn.

## Prerequisites

* [Docker Desktop](https://docs.docker.com/get-docker/) or the Docker Engine + Docker Compose Plugin
* (Optional) A Heroku account and the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) configured with Container Registry access

## 1. Build the image locally

```bash
docker build -t mijourn-web .
```

The build step installs packages from [`Journal/requirements.txt`](Journal/requirements.txt) and runs `python Journal/manage.py collectstatic --noinput` inside the image so static assets are bundled with the container.

## 2. Run the container locally

Create a `.env.docker` file (or adjust the environment in the command below) with the Django settings you need:

```dotenv
SECRET_KEY=changeme-in-development
DATABASE_URL=postgres://journal:journal@db:5432/journal
```

Run the container by itself using SQLite (the default when `DATABASE_URL` is omitted):

```bash
docker run --env-file .env.docker -p 8000:8000 mijourn-web
```

The app will be available at <http://localhost:8000>.

## 3. Run with Postgres using Docker Compose

`docker-compose.yml` defines a two-service stack (`web` + `db`) for local parity with Heroku. Start both services (rebuilding the image if necessary) with:

```bash
docker compose up --build
```

The Postgres service exposes credentials that match the default `DATABASE_URL` in the Compose file. Update the environment values as needed and rerun `docker compose up` to apply the changes.

## 4. Deploy to Heroku Container Registry

1. Log in to Heroku and the Container Registry:

   ```bash
   heroku login
   heroku container:login
   ```

2. Set the app name in an environment variable for convenience:

   ```bash
   export HEROKU_APP=<your-heroku-app-name>
   ```

3. Build and push the image to Heroku:

   ```bash
   docker build -t registry.heroku.com/$HEROKU_APP/web .
   docker push registry.heroku.com/$HEROKU_APP/web
   ```

4. Release the container on Heroku:

   ```bash
   heroku container:release web --app $HEROKU_APP
   ```

Remember to configure required environment variables (e.g., `SECRET_KEY`, OAuth credentials, and any database URLs) in Heroku before releasing the container.
