FROM python:3.14

RUN apt update && apt install -y git vim

COPY requirements.txt ./

RUN pip install -r requirements.txt