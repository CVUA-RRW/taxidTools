FROM ubuntu:22.04

LABEL authors="Gregoire Denay" \
      description="Docker image to run this package"

RUN apt-get -y update
RUN apt-get -y install python3-pip

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install taxidtools
