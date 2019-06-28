#!/usr/bin/env bash

# 跳板机器
proxy bridge -p ":33080" -C ~/proxy/proxy.crt -K ~/proxy/proxy.key --forever --log proxy_bridge.log --daemon
