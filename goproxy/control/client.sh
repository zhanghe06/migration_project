#!/usr/bin/env bash

# 目标机器
proxy client -P "39.100.99.152:33080" -C ~/proxy/proxy.crt -K ~/proxy/proxy.key --forever --log proxy_client.log --daemon
