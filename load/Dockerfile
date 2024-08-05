# Note, the build MUST be executed from the root directory of the repository
# in the local dev environment this is likely the directory ~/chiller.

FROM debian:bookworm

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt update
RUN apt install -y python3-selenium
RUN apt install -y chromium-driver
#RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata
# RUN pip install --upgrade pip
# RUN pip install selenium

COPY ./load/*.py /usr/src/app/

ENTRYPOINT python3 test_wac.py
