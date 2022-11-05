FROM python:3.7
LABEL maintainer="Wolfgang Beer @wolfgangB33r"

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install libgl1

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 run.py