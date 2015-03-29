FROM python:3.4.3-wheezy
MAINTAINER Greg Jeckell, gregory.jeckell@gmail.com

RUN apt-get install -y \
    build-essential

RUN curl -sl https://deb.nodesource.com/setup | bash -

RUN apt-get install -y nodejs

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3.4 install -r requirements.txt
ADD . /code/
