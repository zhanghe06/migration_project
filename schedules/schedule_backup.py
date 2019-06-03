#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: schedule_backup.py
@time: 2019-05-31 15:43
"""

import schedule
import time
from tools.decorator import catch_keyboard_interrupt

from tasks import task_backup

# 数据备份
schedule.every().day.at('02:00').do(task_backup.backup)


@catch_keyboard_interrupt
def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
