FROM python:3.10

# SET USER
USER root

# SET ENVIRONMENT VARIABLES
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# INSTALL REQUIREMENTS
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

# CREATE DIRECTORY
ENV APP_HOME=/misc/django_api_server
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/log
RUN mkdir -p $APP_HOME/run

# SET WORKING DIRECTORY
WORKDIR $APP_HOME

# COPY FILES
COPY . .

# PORT
EXPOSE 8000

# ENTRYPOINT
RUN chmod +x $APP_HOME/deploy/dev/django/entrypoint.sh

ENTRYPOINT [ "/misc/django_api_server/deploy/dev/django/entrypoint.sh" ]