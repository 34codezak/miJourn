# miJourn

## Project Overview
miJourn is a Django-based journaling application composed of two core apps—`entries` and `user`—that together provide authenticated journaling workflows. Users can sign up or log in, create rich journal entries, organize them with tags, update or delete past reflections, and run keyword searches to rediscover previous thoughts.

### Key Features
- **Authentication & profiles:** User management is handled by the `Journal/user` app, enabling secure login, logout, and profile flows.
- **Journal entry CRUD:** The `Journal/entries` app offers forms and views for creating, reading, updating, and deleting journal entries.
- **Tagging & organization:** Entries support tagging, helping users categorize their writing.
- **Search:** Keyword search endpoints surface relevant entries quickly, keeping past insights accessible.

## Prerequisites
- Python 3.12 or newer
- PostgreSQL 14+ (optional; SQLite works out of the box for local development)
- Recommended: `virtualenv` or `venv` for isolated Python environments

## Initial Setup
All commands below assume you are working from the project root (`/workspace/miJourn`).

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies from `Journal/requirements.txt`:**
   ```bash
   pip install --upgrade pip
   pip install -r Journal/requirements.txt
   ```

## Environment Configuration
The Django settings file (`Journal/Journal/settings.py`) reads several environment variables. Create a `.env` file or export these values before running the server.

| Variable | Purpose | Local Development Guidance |
| --- | --- | --- |
| `SECRET_KEY` | Cryptographic secret used by Django. | Set to any long random string in development. Required for production deployments. |
| `DATABASE_URL` | Connection string parsed by `dj-database-url`. | Optional when using the default SQLite database. For PostgreSQL use `postgres://USER:PASSWORD@HOST:PORT/DB_NAME`. |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` | SMTP configuration for outbound email. | Optional; update with your mail provider credentials if you need to send email locally. |
| `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` / `_SECRET`, `SOCIAL_AUTH_FACEBOOK_KEY` / `_SECRET`, `SOCIAL_AUTH_TWITTER_KEY` / `_SECRET`, `SOCIAL_AUTH_GITHUB_KEY` / `_SECRET` | OAuth client credentials for social login backends registered in `AUTHENTICATION_BACKENDS`. | Optional; only required if you enable the corresponding social authentication provider. |

If you do not supply `DATABASE_URL`, Django falls back to the bundled SQLite database (`Journal/db.sqlite3`). To use PostgreSQL locally, ensure the database exists and the user has create privileges, then provide the `DATABASE_URL` value before running migrations.

Example `.env` snippet for local PostgreSQL development:
```env
SECRET_KEY=change-me-in-dev
DATABASE_URL=postgres://journal:journal@localhost:5432/journal
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=secret
EMAIL_USE_TLS=True
```

Load the environment file with a tool like `python-dotenv` or export the variables manually:
```bash
export $(grep -v '^#' .env | xargs)
```

## Database Setup
Run database migrations from the Django project directory (`/workspace/miJourn/Journal`):
```bash
cd Journal
python manage.py makemigrations
python manage.py migrate
```

## Create a Local User Account
Create a superuser (or regular user) so you can log in:
```bash
python manage.py createsuperuser --username demo --email demo@example.com
```
When prompted, enter a password (e.g., `demo12345`). Use these credentials to sign in at [`/user/login/`](http://localhost:8000/user/login/).

## Running the Development Server
From the `Journal/` directory, start Django’s development server:
```bash
python manage.py runserver
```
The application will be available at `http://localhost:8000/`.

### Example Usage Flow
1. **Sign in:** Visit `/user/login/` and enter the credentials you created (`demo` / `demo12345`).
2. **Create an entry:** Navigate to `/entries/create/`, add your journal content, and submit the form.
3. **View or edit an entry:** Visit `/entries/<id>/` (replace `<id>` with the entry’s numeric identifier) to see the detail page; from there you can update or delete the entry.
4. **Search your journal:** Use `/entries/search/` to run keyword searches across your saved entries.

## Optional Tools and Endpoints
- **Run automated tests:**
  ```bash
  python manage.py test
  ```
- **Access the Django admin:** Visit `/admin/` (use the superuser credentials created earlier).
- **Explore API serializers:** The project ships with DRF serializers in `entries/serializers.py` for integrating API endpoints or external clients.

Happy journaling!
