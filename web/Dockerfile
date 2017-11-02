FROM python:3.6.0

RUN mkdir /app
RUN mkdir /app/run
RUN mkdir /app/media
RUN mkdir /app/static
WORKDIR /app
ADD . /app/


RUN pip install -r requirements.txt
