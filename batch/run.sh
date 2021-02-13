#!/bin/bash
docker run --rm \
	-v /Users/lxd/Documents/Code/gaming-analytics/batch/logs:/logs \
	-e "LOGDIR=/logs" \
	-e "BACKUPS=5" \
	-e "SIZE=10485760" \
	-e "INTERVAL=10" \
	-e "MY_NODE_NAME=localhost" \
	-e "MY_POD_NAME=nginx" \
	-it gameserver:0.2



docker run -it --rm \
	-v /Users/lxd/Documents/Code/gaming-analytics/batch/fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf \
	-v /Users/lxd/Documents/Code/gaming-analytics/batch/parsers.conf:/fluent-bit/etc/parsers.conf \
	-v /Users/lxd/Documents/Code/gaming-analytics/batch/plugins.conf:/fluent-bit/etc/plugins.conf \
	-v /Users/lxd/lxd-project.json:/fluent-bit/etc/key.json \
	-v /Users/lxd/Documents/Code/gaming-analytics/batch/logs:/logs \
	-v /Users/lxd/Documents/Code/gaming-analytics/batch/out_gcs.so:/fluent-bit/bin/out_gcs.so \
	-e "GOOGLE_SERVICE_CREDENTIALS=/fluent-bit/etc/key.json" \
	fluent/fluent-bit:1.6 /fluent-bit/bin/fluent-bit \
	-c /fluent-bit/etc/fluent-bit.conf \
	-f 1

docker run -it --rm \
	-v /Users/lxd/lxd-project.json:/fluent-bit/etc/key.json \
	-e "GOOGLE_SERVICE_CREDENTIALS=/fluent-bit/etc/key.json" \
	fluent-bit:1.6