#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_schedule_01.py
@time: 2019-08-21 23:44
"""


import schedule
import time


def job1():
    print("Job1, I'm working...")
    print(time.strftime('%Y-%m-%d %H:%M:%S'))


def job2():
    print("Job2, I'm working...")
    print(time.strftime('%Y-%m-%d %H:%M:%S'))


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
# 场景一: 任务执行时间不超过调度频率，任务频率相同

start
2019-08-22 00:11:26
2019-08-22 00:11:26
end

Job1, I'm working...
2019-08-22 00:11:31
Job2, I'm working...
2019-08-22 00:11:31

Job1, I'm working...
2019-08-22 00:11:36
Job2, I'm working...
2019-08-22 00:11:36
"""
