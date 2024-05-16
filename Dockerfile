# First stage: Build the base image for Django and Poetry
FROM python:3.11 as python-base

# Environment variable configuration
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV DJANGO_SETTINGS_MODULE="config.settings.base"

# Working directory
WORKDIR /app

# Copy Poetry configuration files
COPY poetry.lock pyproject.toml /app/

# Install Poetry and project dependencies
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Second stage: Build the image for development
FROM python-base as development

# Copy the application source code
COPY . /app/

# Third stage: Build the image for the Django development server
FROM development as development-api

# Command to run migrations and start the UVicorn server
CMD python manage.py migrate; uvicorn config.asgi:fastapp --host 0.0.0.0 --port 8500 --reload

# Fourth stage: Build the image for the Django development web server
FROM development as development-web

# Port used by the Django development server
EXPOSE 8000

RUN rm /app/.env

# Run Django migrations and collect static files
RUN python manage.py collectstatic --noinput
COPY .env /app/


# Expose the production server port
EXPOSE 8000

# Add and set permissions for scripts
ADD run.sh /
RUN chmod +x /run.sh

# Run Django collectstatic during image build
RUN python manage.py collectstatic --noinput

# Set the default command to run the application
CMD ["/run.sh"]
