ARG VERSION

FROM ubuntu:focal AS builder

RUN apt-get update && \
    apt-get install curl -y && \
    curl -L https://s3.amazonaws.com/files.molo.ch/builds/ubuntu-20.04/arkime_$VERSION-1_amd64.deb -O

FROM ubuntu:focal

COPY --from=builder /arkime_$VERSION-1_amd64.deb /arkime_$VERSION-1_amd64.deb

RUN apt-get update && \
    apt-get install -y libmagic1 && \
    (dpkg -i *.deb || true) && \
    apt-get install -f -y && \
    rm *.deb && \
    apt-get clean
