#!/usr/bin/env bash

LOCAL_APP_IP='0.0.0.0'
LOCAL_APP_PORT=3366

REMOTE_SSH_USER='root'
REMOTE_SSH_IP='192.168.1.100'
REMOTE_SSH_PORT=22

REMOTE_APP_IP='127.0.0.1'
REMOTE_APP_PORT=3306

echo ssh \
    -f \
    ${REMOTE_SSH_USER}@${REMOTE_SSH_IP} \
    -p ${REMOTE_SSH_PORT}  \
    -L ${LOCAL_APP_IP}:${LOCAL_APP_PORT}:${REMOTE_APP_IP}:${REMOTE_APP_PORT} \
    -N

ssh \
    -f \
    ${REMOTE_SSH_USER}@${REMOTE_SSH_IP} \
    -p ${REMOTE_SSH_PORT} \
    -L ${LOCAL_APP_IP}:${LOCAL_APP_PORT}:${REMOTE_APP_IP}:${REMOTE_APP_PORT} \
    -N

netstat -ant | grep ${LOCAL_APP_PORT}