FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /sc_backend

WORKDIR /sc_backend

RUN pip install pip -U

ADD requirements.txt /sc_backend/

RUN pip install -r requirements.txt

ADD . /sc_backend/