# pull official base image
# FROM python:3.9-alpine
FROM python:3.7
# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN useradd -u 8877 myuser
USER myuser

# run gunicorn
#comment this in Heroku deployment
#CMD gunicorn pytorch_django.wsgi:application --bind 0.0.0.0:$PORT