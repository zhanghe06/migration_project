#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: schedule_backup.py
@time: 2019-05-31 15:43
"""

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
from tools.decorator import catch_keyboard_interrupt


@catch_keyboard_interrupt
def run():
    task_migration_user.migration_user()
    task_migration_customer.migration_customer()
    task_migration_supplier.migration_supplier()
    task_migration_warehouse.migration_warehouse()
    task_migration_rack.migration_rack()
    task_migration_production.migration_production()
    task_migration_inventory.migration_inventory()
    task_migration_delivery.migration_delivery()
    task_migration_purchase.migration_purchase()


if __name__ == '__main__':
    run()
