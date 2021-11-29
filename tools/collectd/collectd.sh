#!/bin/bash

sed -i "s/HOSTNAME/$HOSTNAME/" /etc/collectd/collectd.conf

collectd -C /etc/collectd/collectd.conf
tail -f /dev/null