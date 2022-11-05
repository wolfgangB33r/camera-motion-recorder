FROM python:3.7
LABEL maintainer="Wolfgang Beer @wolfgangB33r"

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 run.py