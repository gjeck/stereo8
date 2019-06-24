FROM ubuntu:18.04
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
    python3-setuptools \
    python3-pip \
    python3-dev \
    curl \
    git \
    vim \
    && apt-get autoremove \
    && apt-get clean

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r stereo8/requirements.txt
