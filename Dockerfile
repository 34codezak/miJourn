# syntax=docker/dockerfile:1

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY Journal/requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files during the image build
RUN python Journal/manage.py collectstatic --noinput

# Expose port for the web server
EXPOSE 8000

# Run the Django app with Gunicorn
CMD ["gunicorn", "Journal.wsgi:application", "--bind", "0.0.0.0:8000"]
