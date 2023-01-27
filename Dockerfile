FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y libpq-dev postgresql

RUN pip install --upgrade pip


WORKDIR /internet_shop_rest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./
RUN pip install -r requirements.txt


COPY . .
