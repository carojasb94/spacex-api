FROM python:3.7

WORKDIR /opt/spacex-api

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy work directory
COPY . .
