# miJourn Deployment Notes

To run this project on Heroku or another WSGI-compatible platform, ensure the following environment variables are set:

- `DJANGO_SETTINGS_MODULE` – typically `Journal.settings`.
- `DATABASE_URL` – connection string for the production database.

Gunicorn will start the app using the command defined in the Procfile.
