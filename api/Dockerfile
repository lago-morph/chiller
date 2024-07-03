FROM python:3.12

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./dist/ /usr/src/app/dist/

RUN pip install chiller_api -f /usr/src/app/dist

RUN pip install gunicorn

EXPOSE 80

ENTRYPOINT gunicorn -w 4 --bind 0.0.0.0:80 'chiller_api:create_app()'
