FROM pataquets/ubuntu:focal

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -y --no-install-recommends install collectd-core libyajl-dev librdkafka-dev \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* \
  && \
  mkdir -vp /etc/collectd/conf.d/

ADD collectd.conf /etc/collectd/
ADD collectd.sh .

ENTRYPOINT  ["./collectd.sh"]