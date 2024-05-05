FROM python:latest

WORKDIR /usr/src/app/

COPY ./docker-entrypoint.sh .
RUN chmod +x ./docker-entrypoint.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .