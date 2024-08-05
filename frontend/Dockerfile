# Note, the build MUST be executed from the root directory of the repository
# in the local dev environment this is likely the directory ~/chiller.

FROM python:3.12

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install gunicorn

COPY ./sdk/dist/ /usr/src/app/sdk/
COPY ./frontend/dist/ /usr/src/app/frontend/

RUN pip install chiller_api_client -f /usr/src/app/sdk
RUN pip install chiller_frontend -f /usr/src/app/frontend

EXPOSE 80

ENTRYPOINT gunicorn --statsd-host=localhost:9125 --statsd-prefix=chiller.frontend -w 4 --bind 0.0.0.0:80 'chiller_frontend:create_app()'
