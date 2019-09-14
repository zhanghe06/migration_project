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
from apps.models.db_source.pu_purchasearrival import PUPurchaseArrival as SourcePurchase
from apps.models.db_source.pu_purchasearrival_b import PUPurchaseArrivalB as SourcePurchaseItems
from apps.models.db_target import Production as TargetProduction
from apps.models.db_target import Purchase as TargetPurchase
from apps.models.db_target import PurchaseItems as TargetPurchaseItems
from apps.models.db_target import Rack as TargetRack
from apps.models.db_target import Supplier as TargetSupplier
from apps.models.db_target import SupplierContact as TargetSupplierContact
from apps.models.db_target import User as TargetUser
from apps.models.db_target import Warehouse as TargetWarehouse
from libs.migration_client import MigrationClient
from maps.type_purchase import TYPE_PURCHASE_NORMAL
from maps.type_tax import TYPE_TAX_HAS, TYPE_TAX_NOT
from tools.date_time import time_local_to_utc


def sync():
    purchase_client = MigrationClient('purchase', SourcePurchase, TargetPurchase, MigrationContrast)
    purchase_items_client = MigrationClient('purchase_items', SourcePurchaseItems, TargetPurchaseItems,
                                            MigrationContrast)
    user_client = MigrationClient('user', SourceUser, TargetUser, MigrationContrast)
    supplier_client = MigrationClient('supplier', None, TargetSupplier, MigrationContrast)
    supplier_contact_client = MigrationClient('supplier_contact', None, TargetSupplierContact, MigrationContrast)
    warehouse_client = MigrationClient('warehouse', None, TargetWarehouse, MigrationContrast)
    rack_client = MigrationClient('rack', None, TargetRack, MigrationContrast)
    production_client = MigrationClient('production', None, TargetProduction, MigrationContrast)

    while 1:
        s_rows = purchase_client.s_api.get_limit_rows_by_last_id(
            last_pk=purchase_client.s_id,
            limit_num=purchase_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            purchase_client.s_data = s_data
            purchase_client.s_id = purchase_client.s_data.id
            purchase_client.latest_time = time_local_to_utc(purchase_client.s_data.updated)

            # ----------
            # 制单人员
            user_client.m_data = user_client.m_api.get_row(
                table_name='user',
                pk_source=purchase_client.s_data.makerid,
            )
            if not user_client.m_data:
                continue

            # 供应商信息
            supplier_client.m_data = supplier_client.m_api.get_row(
                table_name='supplier',
                pk_source=purchase_client.s_data.idpartner,
            )
            if not supplier_client.m_data:
                continue
            supplier_client.t_data = supplier_client.t_api.get_row_by_id(supplier_client.m_data.pk_target)
            if not supplier_client.t_data:
                continue
            # 联系方式
            supplier_contact_client.t_data = supplier_contact_client.t_api.get_row(
                cid=supplier_client.m_data.pk_target,
            )
            if not supplier_contact_client.t_data:
                continue
            # 仓库
            warehouse_client.m_data = warehouse_client.m_api.get_row(
                table_name='warehouse',
                pk_source=purchase_client.s_data.idwarehouse,
            )
            if not warehouse_client.m_data:
                continue
            # ----------

            purchase_client.m_detail()
            # 存在历史数据
            if purchase_client.m_data:
                if purchase_client.latest_time <= purchase_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                purchase_client.t_id = purchase_client.m_data.pk_target
                current_time = datetime.utcnow()
                purchase_client.t_data = {
                    'uid': user_client.m_data.pk_target,
                    'supplier_cid': supplier_client.t_data.id,
                    'supplier_company_name': supplier_client.t_data.company_name,
                    'supplier_contact_id': supplier_contact_client.t_data.id,
                    'type_purchase': TYPE_PURCHASE_NORMAL,
                    'amount_production': purchase_client.s_data.totalTaxAmount,
                    'amount_purchase': purchase_client.s_data.totalTaxAmount,
                    'warehouse_id': warehouse_client.m_data.pk_target,
                    'note': purchase_client.s_data.memo,
                    'type_tax': TYPE_TAX_HAS if purchase_client.s_data.totalTaxAmount > purchase_client.s_data.totalAmount else TYPE_TAX_NOT,
                    'update_time': time_local_to_utc(purchase_client.s_data.updated),  # 本地时间修改为UTC时间
                }
                # 删除条件
                # if purchase_client.s_data.disabled:
                #     purchase_client.t_data['status_delete'] = True
                #     purchase_client.t_data['delete_time'] = current_time
                # ----------
                purchase_client.t_update()
                purchase_client.m_update()

                # 明细数据
                # 清空历史
                purchase_items_history_rows = purchase_items_client.t_api.get_rows()
                for purchase_items_history_data in purchase_items_history_rows:
                    purchase_items_client.t_api.delete(purchase_items_history_data.id)
                # 全部更新
                s_i_rows = purchase_items_client.s_api.get_rows(idPurchaseArrivalDTO=purchase_client.s_data.id)
                for s_i_data in s_i_rows:
                    purchase_items_client.s_data = s_i_data
                    purchase_items_client.s_id = purchase_items_client.s_data.id
                    purchase_items_client.latest_time = time_local_to_utc(purchase_client.s_data.updated)
                    # 产品
                    production_client.m_data = production_client.m_api.get_row(
                        table_name='production',
                        pk_source=purchase_items_client.s_data.idinventory,
                    )
                    if not production_client.m_data:
                        continue
                    production_client.t_data = production_client.t_api.get_row_by_id(production_client.m_data.pk_target)
                    if not production_client.t_data:
                        continue
                    # 仓位
                    rack_client.m_data = rack_client.m_api.get_row(
                        table_name='rack',
                        pk_source=purchase_items_client.s_data.inventoryLocation,
                    )

                    # 更新明细
                    purchase_items_client.t_data = {
                        'purchase_id': purchase_client.t_id,
                        'uid': user_client.m_data.pk_target,
                        'supplier_cid': supplier_client.t_data.id,
                        'supplier_company_name': supplier_client.t_data.company_name,
                        'production_id': production_client.t_data.id,
                        'production_brand': production_client.t_data.production_brand,
                        'production_model': production_client.t_data.production_model,
                        'production_sku': production_client.t_data.production_sku,
                        'warehouse_id': warehouse_client.m_data.pk_target,
                        'rack_id': rack_client.m_data.pk_target if rack_client.m_data else 0,
                        'type_tax': TYPE_TAX_HAS if purchase_client.s_data.totalTaxAmount > purchase_client.s_data.totalAmount else TYPE_TAX_NOT,
                        'quantity': purchase_items_client.s_data.quantity,
                        'unit_price': purchase_items_client.s_data.taxPrice,
                        'create_time': time_local_to_utc(purchase_client.s_data.createdtime),  # 本地时间修改为UTC时间
                        'update_time': time_local_to_utc(purchase_client.s_data.updated),  # 本地时间修改为UTC时间
                    }
                    # 删除条件 Fixme
                    # if purchase_client.s_data.disabled:
                    #     current_time = datetime.utcnow()
                    #     purchase_items_client.t_data['status_delete'] = True,
                    #     purchase_items_client.t_data['delete_time'] = current_time,

                    purchase_items_client.t_create()

            # 没有历史数据
            else:
                # 目标数据去重
                # purchase_client.t_data = purchase_client.t_api.get_row(name=purchase_client.s_data.name)
                # if purchase_client.t_data:
                #     continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                purchase_client.t_data = {
                    'uid': user_client.m_data.pk_target,
                    'supplier_cid': supplier_client.t_data.id,
                    'supplier_company_name': supplier_client.t_data.company_name,
                    'supplier_contact_id': supplier_contact_client.t_data.id,
                    'type_purchase': TYPE_PURCHASE_NORMAL,
                    'amount_production': purchase_client.s_data.totalTaxAmount,
                    'amount_purchase': purchase_client.s_data.totalTaxAmount,
                    'warehouse_id': warehouse_client.m_data.pk_target,
                    'note': purchase_client.s_data.memo,
                    'type_tax': TYPE_TAX_HAS if purchase_client.s_data.totalTaxAmount > purchase_client.s_data.totalAmount else TYPE_TAX_NOT,
                    'create_time': time_local_to_utc(purchase_client.s_data.createdtime),  # 本地时间修改为UTC时间
                    'update_time': time_local_to_utc(purchase_client.s_data.updated),  # 本地时间修改为UTC时间
                }
                # 删除条件
                # if purchase_client.s_data.disabled:
                #     purchase_client.t_data['status_delete'] = True
                #     purchase_client.t_data['delete_time'] = current_time
                # ----------
                purchase_client.t_create()
                purchase_client.m_create()

                # 明细数据
                s_i_rows = purchase_items_client.s_api.get_rows(idPurchaseArrivalDTO=purchase_client.s_data.id)
                for s_i_data in s_i_rows:
                    purchase_items_client.s_data = s_i_data
                    purchase_items_client.s_id = purchase_items_client.s_data.id
                    purchase_items_client.latest_time = time_local_to_utc(purchase_client.s_data.updated)
                    # 产品
                    production_client.m_data = production_client.m_api.get_row(
                        table_name='production',
                        pk_source=purchase_items_client.s_data.idinventory,
                    )
                    if not production_client.m_data:
                        continue
                    production_client.t_data = production_client.t_api.get_row_by_id(production_client.m_data.pk_target)
                    if not production_client.t_data:
                        continue
                    # 仓位
                    rack_client.m_data = rack_client.m_api.get_row(
                        table_name='rack',
                        pk_source=purchase_items_client.s_data.inventoryLocation,
                    )

                    # 插入明细
                    purchase_items_client.t_data = {
                        'purchase_id': purchase_client.t_id,
                        'uid': user_client.m_data.pk_target,
                        'supplier_cid': supplier_client.t_data.id,
                        'supplier_company_name': supplier_client.t_data.company_name,
                        'production_id': production_client.t_data.id,
                        'production_brand': production_client.t_data.production_brand,
                        'production_model': production_client.t_data.production_model,
                        'production_sku': production_client.t_data.production_sku,
                        'warehouse_id': warehouse_client.m_data.pk_target,
                        'rack_id': rack_client.m_data.pk_target if rack_client.m_data else 0,
                        'type_tax': TYPE_TAX_HAS if purchase_client.s_data.totalTaxAmount > purchase_client.s_data.totalAmount else TYPE_TAX_NOT,
                        'quantity': purchase_items_client.s_data.quantity,
                        'unit_price': purchase_items_client.s_data.taxPrice,
                        'create_time': time_local_to_utc(purchase_client.s_data.createdtime),  # 本地时间修改为UTC时间
                        'update_time': time_local_to_utc(purchase_client.s_data.updated),  # 本地时间修改为UTC时间
                    }
                    # 删除条件 Fixme
                    # if purchase_client.s_data.disabled:
                    #     current_time = datetime.utcnow()
                    #     purchase_items_client.t_data['status_delete'] = True,
                    #     purchase_items_client.t_data['delete_time'] = current_time,

                    purchase_items_client.t_create()

    result = {
        '来源总数': purchase_client.s_api.count(),
        '目标总数': purchase_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
