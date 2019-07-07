FROM ubuntu:19.10

VOLUME /src/python/current

RUN apt-get update&& apt-get install --assume-yes python3 \
  python3-dev \
  python3-pip \
  imagemagick

RUN pip3 install docopt \
  coloredlogs \
  sh \
  numpy \
  Pillow

COPY src /src

CMD python3 /src/python/cli.py
