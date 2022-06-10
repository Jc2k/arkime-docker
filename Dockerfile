ARG VERSION

FROM ubuntu:focal AS builder

RUN apt-get update && \
    apt-get install curl -y && \
    curl https://s3.amazonaws.com/files.molo.ch/builds/ubuntu-20.04/moloch_$VERSION-1_amd64.deb -O

FROM ubuntu:focal

COPY --from=builder /moloch_$VERSION-1_amd64.deb /moloch_$VERSION-1_amd64.deb

RUN apt-get install -y libmagic1 && \
    (dpkg -i *.deb || true) && \
    apt-get install -f -y && \
    rm *.deb
