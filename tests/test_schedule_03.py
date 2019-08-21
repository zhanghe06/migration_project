#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_schedule_03.py
@time: 2019-08-21 23:44
"""


import schedule
import time


def job1():
    print("Job1, I'm working...")
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(10)


def job2():
    print("Job2, I'm working...")
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(10)


def run():
    print("start")
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    schedule.every(5).seconds.do(job1)
    schedule.every(5).seconds.do(job2)
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print("end\n")

    while True:
        schedule.run_pending()
        time.sleep(1)  # 调度间隔


if __name__ == '__main__':
    run()


"""
# 场景三: 任务执行时间超过调度频率，任务频率相同

start
2019-08-22 00:16:40
2019-08-22 00:16:40
end

Job1, I'm working...
2019-08-22 00:16:45
Job2, I'm working...
2019-08-22 00:16:55

Job1, I'm working...
2019-08-22 00:17:06
Job2, I'm working...
2019-08-22 00:17:17

Job1, I'm working...
2019-08-22 00:17:28
Job2, I'm working...
2019-08-22 00:17:39
"""
