#FROM python:3.7
FROM python:3.10-slim-bullseye
LABEL maintainer="Wolfgang Beer @wolfgangB33r"

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 run.py
