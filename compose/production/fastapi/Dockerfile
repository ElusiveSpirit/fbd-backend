FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # dependencies for ansible
  && echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" >> /etc/apt/sources.list \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 \
  && apt-get update \
  && apt-get install -y ansible ssh \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system fastapi \
    && adduser --system --ingroup fastapi fastapi

RUN pip install pipenv

# Requirements are installed here to ensure they will be cached.
COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock
RUN pipenv install --system --deploy

COPY ./compose/production/fastapi/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown fastapi /entrypoint

COPY ./compose/production/fastapi/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown fastapi /start

COPY ./compose/production/fastapi/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown fastapi /start-celeryworker

COPY ./compose/production/fastapi/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown fastapi /start-celerybeat

COPY --chown=fastapi:fastapi . /app

USER fastapi

WORKDIR /app

ENTRYPOINT ["/entrypoint"]