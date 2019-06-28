#!/usr/bin/env bash

# 本地机器
proxy server -r ":2202@:22" -P "39.100.99.152:33080" -C ~/proxy/proxy.crt -K ~/proxy/proxy.key --forever --log proxy_server.log --daemon
