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

from tasks import (
    task_migration_user,
    task_migration_customer,
    task_migration_supplier,
    task_migration_delivery,
    task_migration_purchase,
    task_migration_warehouse,
    task_migration_rack,
    task_migration_production,
    task_migration_inventory,
)

# 立即执行
task_migration_user.migration_user()
task_migration_customer.migration_customer()
task_migration_supplier.migration_supplier()
task_migration_warehouse.migration_warehouse()
task_migration_rack.migration_rack()
task_migration_production.migration_production()
task_migration_inventory.migration_inventory()
task_migration_delivery.migration_delivery()
task_migration_purchase.migration_purchase()


# 定时任务

# 同步用户
schedule.every(30).minutes.do(task_migration_user.migration_user)

# 同步客户
schedule.every(30).minutes.do(task_migration_customer.migration_customer)
# 同步友商
schedule.every(30).minutes.do(task_migration_supplier.migration_supplier)

# 同步仓库
schedule.every(30).minutes.do(task_migration_warehouse.migration_warehouse)
# 同步仓位
schedule.every(30).minutes.do(task_migration_rack.migration_rack)

# 同步产品
schedule.every(30).minutes.do(task_migration_production.migration_production)
# 同步库存
schedule.every(30).minutes.do(task_migration_inventory.migration_inventory)

# 同步销货
schedule.every(30).minutes.do(task_migration_delivery.migration_delivery)
# 同步进货
schedule.every(30).minutes.do(task_migration_purchase.migration_purchase)


@catch_keyboard_interrupt
def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
