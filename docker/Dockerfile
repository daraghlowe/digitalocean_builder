FROM python:3.7
ENV PYTHONUNBUFFERED 1

WORKDIR /digitalocean-builder

# Install required python packages
COPY digitalocean-builder/requirements.indexes /digitalocean-builder/
COPY digitalocean-builder/requirements.txt /digitalocean-builder/
RUN pip install -r requirements.txt

# Django app code
COPY ./digitalocean-builder/ /digitalocean-builder/

# Static file support
RUN mkdir -p /var/www/static/
RUN DJANGO_SETTINGS_MODULE=config.settings.dev ./manage.py collectstatic --no-input

# These are defined in Jenkins ENV variables and passed in through docker-compose
ARG GIT_COMMIT=unknown
ARG BUILD_NUMBER=unknown

ENV VERSION="0.1.${BUILD_NUMBER}"
ENV GIT_COMMIT=$GIT_COMMIT

# DONT run as ROOT
RUN useradd -ms /bin/bash app
RUN chown -R app:app /digitalocean-builder
USER app

CMD /digitalocean-builder/bin/web.sh
