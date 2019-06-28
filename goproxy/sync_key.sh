#!/usr/bin/env bash

# 拷贝B机器的公钥和秘钥文件
mkdir -p ~/proxy
scp -r root@39.100.99.152:~/proxy ~
# scp -i ~/.ssh/id_rsa -r root@39.100.99.152:~/proxy ~
