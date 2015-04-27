FROM ubuntu:14.04
MAINTAINER Greg Jeckell, gregory.jeckell@gmail.com

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y -q \
    build-essential \
    libpq-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    lib32z1-dev \
    libssl-dev \
    pkg-config \
    gcc \
    make \
    python3.4 \
    python3.4-dev \
    python-dev \
    python3-pip \
    python-pip \
    curl \
    git \
    vim \
    nodejs \
    npm \
    && apt-get autoremove \
    && apt-get clean

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip3 install -r stereo8/requirements.txt
RUN pip install -r scrapers/requirements.txt
