FROM python:3.6.0

RUN mkdir -p /app/run
RUN mkdir /app/media
RUN mkdir /app/static
WORKDIR /app
ADD . /app/

RUN pip install -r requirements.txt
RUN pip install -e git+https://github.com/MongoEngine/django-mongoengine#egg=django_mongoengine
