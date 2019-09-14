#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-09-14 18:18
"""

from __future__ import unicode_literals

from datetime import datetime

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.eap_user import EAPUser as SourceUser
from apps.models.db_source.sa_saledelivery import SASaleDelivery as SourceDelivery
from apps.models.db_source.sa_saledelivery_b import SASaleDeliveryB as SourceDeliveryItems
from apps.models.db_target import Customer as TargetCustomer
from apps.models.db_target import CustomerContact as TargetCustomerContact
from apps.models.db_target import Delivery as TargetDelivery
from apps.models.db_target import DeliveryItems as TargetDeliveryItems
from apps.models.db_target import Production as TargetProduction
from apps.models.db_target import Rack as TargetRack
from apps.models.db_target import User as TargetUser
from apps.models.db_target import Warehouse as TargetWarehouse
from libs.migration_client import MigrationClient
from maps.type_delivery import TYPE_DELIVERY_NORMAL
from maps.type_tax import TYPE_TAX_HAS, TYPE_TAX_NOT
from tools.date_time import time_local_to_utc


def sync():
    delivery_client = MigrationClient('delivery', SourceDelivery, TargetDelivery, MigrationContrast)
    delivery_items_client = MigrationClient('delivery_items', SourceDeliveryItems, TargetDeliveryItems,
                                            MigrationContrast)
    user_client = MigrationClient('user', SourceUser, TargetUser, MigrationContrast)
    customer_client = MigrationClient('customer', None, TargetCustomer, MigrationContrast)
    customer_contact_client = MigrationClient('customer_contact', None, TargetCustomerContact, MigrationContrast)
    warehouse_client = MigrationClient('warehouse', None, TargetWarehouse, MigrationContrast)
    rack_client = MigrationClient('rack', None, TargetRack, MigrationContrast)
    production_client = MigrationClient('production', None, TargetProduction, MigrationContrast)

    while 1:
        s_rows = delivery_client.s_api.get_limit_rows_by_last_id(
            last_pk=delivery_client.s_id,
            limit_num=delivery_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            delivery_client.s_data = s_data
            delivery_client.s_id = delivery_client.s_data.id
            delivery_client.latest_time = time_local_to_utc(delivery_client.s_data.updated)

            # ----------
            # 制单人员
            user_client.m_data = user_client.m_api.get_row(
                table_name='user',
                pk_source=delivery_client.s_data.makerid,
            )
            if not user_client.m_data:
                continue

            # 客户信息
            customer_client.m_data = customer_client.m_api.get_row(
                table_name='customer',
                pk_source=delivery_client.s_data.idsettleCustomer,
            )
            if not customer_client.m_data:
                continue
            customer_client.t_data = customer_client.t_api.get_row_by_id(customer_client.m_data.pk_target)
            if not customer_client.t_data:
                continue
            # 联系方式
            customer_contact_client.t_data = customer_contact_client.t_api.get_row(
                cid=customer_client.m_data.pk_target,
            )
            if not customer_contact_client.t_data:
                continue
            # 仓库
            warehouse_client.m_data = warehouse_client.m_api.get_row(
                table_name='warehouse',
                pk_source=delivery_client.s_data.idwarehouse,
            )
            if not warehouse_client.m_data:
                continue
            # ----------

            delivery_client.m_detail()
            # 存在历史数据
            if delivery_client.m_data:
                if delivery_client.latest_time <= delivery_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                delivery_client.t_id = delivery_client.m_data.pk_target
                current_time = datetime.utcnow()
                delivery_client.t_data = {
                    'uid': user_client.m_data.pk_target,
                    'customer_cid': customer_client.t_data.id,
                    'customer_company_name': customer_client.t_data.company_name,
                    'customer_contact_id': customer_contact_client.t_data.id,
                    'type_delivery': TYPE_DELIVERY_NORMAL,
                    'amount_production': delivery_client.s_data.taxAmount,
                    'amount_delivery': delivery_client.s_data.taxAmount,
                    'warehouse_id': warehouse_client.m_data.pk_target,
                    'note': delivery_client.s_data.memo,
                    'type_tax': TYPE_TAX_HAS if delivery_client.s_data.taxAmount > delivery_client.s_data.amount else TYPE_TAX_NOT,
                    'update_time': time_local_to_utc(delivery_client.s_data.updated),  # 本地时间修改为UTC时间
                }
                # 删除条件
                # if delivery_client.s_data.disabled:
                #     delivery_client.t_data['status_delete'] = True
                #     delivery_client.t_data['delete_time'] = current_time
                # ----------
                delivery_client.t_update()
                delivery_client.m_update()

                # 明细数据
                # 清空历史
                delivery_items_history_rows = delivery_items_client.t_api.get_rows()
                for delivery_items_history_data in delivery_items_history_rows:
                    delivery_items_client.t_api.delete(delivery_items_history_data.id)
                # 全部更新
                s_i_rows = delivery_items_client.s_api.get_rows(idSaleDeliveryDTO=delivery_client.s_data.id)
                for s_i_data in s_i_rows:
                    delivery_items_client.s_data = s_i_data
                    delivery_items_client.s_id = delivery_items_client.s_data.id
                    delivery_items_client.latest_time = time_local_to_utc(delivery_client.s_data.updated)
                    # 产品
                    production_client.m_data = production_client.m_api.get_row(
                        table_name='production',
                        pk_source=delivery_items_client.s_data.idinventory,
                    )
                    if not production_client.m_data:
                        continue
                    production_client.t_data = production_client.t_api.get_row_by_id(production_client.m_data.pk_target)
                    if not production_client.t_data:
                        continue
                    # 仓位
                    rack_client.m_data = rack_client.m_api.get_row(
                        table_name='rack',
                        pk_source=delivery_items_client.s_data.inventoryLocation,
                    )

                    # 更新明细
                    delivery_items_client.t_data = {
                        'delivery_id': delivery_client.t_id,
                        'uid': user_client.m_data.pk_target,
                        'customer_cid': customer_client.t_data.id,
                        'customer_company_name': customer_client.t_data.company_name,
                        'production_id': production_client.t_data.id,
                        'production_brand': production_client.t_data.production_brand,
                        'production_model': production_client.t_data.production_model,
                        'production_sku': production_client.t_data.production_sku,
                        'warehouse_id': warehouse_client.m_data.pk_target,
                        'rack_id': rack_client.m_data.pk_target if rack_client.m_data else 0,
                        'type_tax': TYPE_TAX_HAS if delivery_client.s_data.taxAmount > delivery_client.s_data.amount else TYPE_TAX_NOT,
                        'quantity': delivery_items_client.s_data.quantity,
                        'unit_price': delivery_items_client.s_data.taxPrice,
                        'create_time': time_local_to_utc(delivery_client.s_data.createdtime),  # 本地时间修改为UTC时间
                        'update_time': time_local_to_utc(delivery_client.s_data.updated),  # 本地时间修改为UTC时间
                    }
                    # 删除条件 Fixme
                    # if delivery_client.s_data.disabled:
                    #     current_time = datetime.utcnow()
                    #     delivery_items_client.t_data['status_delete'] = True,
                    #     delivery_items_client.t_data['delete_time'] = current_time,

                    delivery_items_client.t_create()

            # 没有历史数据
            else:
                # 目标数据去重
                # delivery_client.t_data = delivery_client.t_api.get_row(name=delivery_client.s_data.name)
                # if delivery_client.t_data:
                #     continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                delivery_client.t_data = {
                    'uid': user_client.m_data.pk_target,
                    'customer_cid': customer_client.t_data.id,
                    'customer_company_name': customer_client.t_data.company_name,
                    'customer_contact_id': customer_contact_client.t_data.id,
                    'type_delivery': TYPE_DELIVERY_NORMAL,
                    'amount_production': delivery_client.s_data.taxAmount,
                    'amount_delivery': delivery_client.s_data.taxAmount,
                    'warehouse_id': warehouse_client.m_data.pk_target,
                    'note': delivery_client.s_data.memo,
                    'type_tax': TYPE_TAX_HAS if delivery_client.s_data.taxAmount > delivery_client.s_data.amount else TYPE_TAX_NOT,
                    'create_time': time_local_to_utc(delivery_client.s_data.createdtime),  # 本地时间修改为UTC时间
                    'update_time': time_local_to_utc(delivery_client.s_data.updated),  # 本地时间修改为UTC时间
                }
                # 删除条件
                # if delivery_client.s_data.disabled:
                #     delivery_client.t_data['status_delete'] = True
                #     delivery_client.t_data['delete_time'] = current_time
                # ----------
                delivery_client.t_create()
                delivery_client.m_create()

                # 明细数据
                s_i_rows = delivery_items_client.s_api.get_rows(idSaleDeliveryDTO=delivery_client.s_data.id)
                for s_i_data in s_i_rows:
                    delivery_items_client.s_data = s_i_data
                    delivery_items_client.s_id = delivery_items_client.s_data.id
                    delivery_items_client.latest_time = time_local_to_utc(delivery_client.s_data.updated)
                    # 产品
                    production_client.m_data = production_client.m_api.get_row(
                        table_name='production',
                        pk_source=delivery_items_client.s_data.idinventory,
                    )
                    if not production_client.m_data:
                        continue
                    production_client.t_data = production_client.t_api.get_row_by_id(production_client.m_data.pk_target)
                    if not production_client.t_data:
                        continue
                    # 仓位
                    rack_client.m_data = rack_client.m_api.get_row(
                        table_name='rack',
                        pk_source=delivery_items_client.s_data.inventoryLocation,
                    )

                    # 插入明细
                    delivery_items_client.t_data = {
                        'delivery_id': delivery_client.t_id,
                        'uid': user_client.m_data.pk_target,
                        'customer_cid': customer_client.t_data.id,
                        'customer_company_name': customer_client.t_data.company_name,
                        'production_id': production_client.t_data.id,
                        'production_brand': production_client.t_data.production_brand,
                        'production_model': production_client.t_data.production_model,
                        'production_sku': production_client.t_data.production_sku,
                        'warehouse_id': warehouse_client.m_data.pk_target,
                        'rack_id': rack_client.m_data.pk_target if rack_client.m_data else 0,
                        'type_tax': TYPE_TAX_HAS if delivery_client.s_data.taxAmount > delivery_client.s_data.amount else TYPE_TAX_NOT,
                        'quantity': delivery_items_client.s_data.quantity,
                        'unit_price': delivery_items_client.s_data.taxPrice,
                        'create_time': time_local_to_utc(delivery_client.s_data.createdtime),  # 本地时间修改为UTC时间
                        'update_time': time_local_to_utc(delivery_client.s_data.updated),  # 本地时间修改为UTC时间
                    }
                    # 删除条件 Fixme
                    # if delivery_client.s_data.disabled:
                    #     current_time = datetime.utcnow()
                    #     delivery_items_client.t_data['status_delete'] = True,
                    #     delivery_items_client.t_data['delete_time'] = current_time,

                    delivery_items_client.t_create()

    result = {
        '来源总数': delivery_client.s_api.count(),
        '目标总数': delivery_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
