#!/usr/bin/env bash

mkdir -p ~/proxy
cd ~/proxy

# 生成自签名的证书和key文件
proxy keygen -C proxy

# 使用自签名证书proxy.crt和key文件proxy.key签发新证书:goproxy.crt和goproxy.key
proxy keygen -s -C proxy -c goproxy
