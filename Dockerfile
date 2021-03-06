FROM ubuntu:focal AS builder

ARG VERSION

RUN apt-get update && \
    apt-get install curl -y && \
    curl -L https://s3.amazonaws.com/files.molo.ch/builds/ubuntu-20.04/arkime_$VERSION-1_amd64.deb -O

FROM ubuntu:focal

ARG VERSION

COPY --from=builder /arkime_$VERSION-1_amd64.deb /arkime_$VERSION-1_amd64.deb

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y iproute2 libmagic1 && \
    (dpkg -i *.deb || true) && \
    apt-get install -f -y && \
    rm *.deb && \
    apt-get clean

COPY arkime_config_interfaces.sh /opt/arkime/bin/arkime_config_interfaces.sh
