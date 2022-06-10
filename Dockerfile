FROM ubuntu:focal

ARG VERSION

RUN apt-get update && \
    apt-get install curl -y && \
    curl https://s3.amazonaws.com/files.molo.ch/builds/ubuntu-20.04/moloch_$VERSION-1_amd64.deb -O && \
    (dpkg -i *.deb || true) && \
    apt-get install -f -y && \
    apt-get install -y libmagic1 && \
    rm *.deb && \
    apt-get remove curl --purge -y && \
    apt-get autoremove --purge -y
