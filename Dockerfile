FROM python:3.11

RUN apt-get update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

WORKDIR /app

COPY . /app

EXPOSE 8000

WORKDIR /app/src

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]