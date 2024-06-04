FROM python:3.11.9-slim

LABEL authors="Gregoire Denay" \
      description="Docker image to run this package"

RUN apt-get -y update

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install taxidtools
