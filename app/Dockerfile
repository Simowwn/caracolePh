FROM python:3.12.7

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install gcc postgresql \
  && apt-get clean \
  && pip install psycopg2-binary

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app

ENTRYPOINT ["/bin/bash", "/usr/src/app/entrypoint.sh"]