# Note, the build MUST be executed from the root directory of the repository
# in the local dev environment this is likely the directory ~/chiller.
FROM python:3.12

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN pip install gunicorn

RUN mkdir -p /usr/src/app/api

COPY ./api/dist/ /usr/src/app/dist/

RUN pip install chiller_api -f /usr/src/app/dist

EXPOSE 80

ENTRYPOINT gunicorn -w 4 --bind 0.0.0.0:80 'chiller_api:create_app()'
