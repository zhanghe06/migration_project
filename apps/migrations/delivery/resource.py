#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-05-07 01:24
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
# from apps.sources.apis.current_stock import (
#     get_current_stock_row_by_id as sources_get_delivery_row_by_id,
#     get_current_stock_limit_rows_by_last_id as sources_get_delivery_limit_rows_by_last_id,
#     count_current_stock as sources_count_delivery,
# )

from apps.sources.apis.sale_delivery import (
    get_sale_delivery_row_by_id as sources_get_delivery_row_by_id,
    get_sale_delivery_limit_rows_by_last_id as sources_get_delivery_limit_rows_by_last_id,
    count_sale_delivery as sources_count_delivery,
)
from apps.sources.apis.sale_delivery_items import (
    get_sale_delivery_items_rows as sources_get_delivery_items_rows,
    # add_sale_delivery_items as sources_add_delivery_items,
)
from apps.targets.warehouse.api import get_warehouse_row_by_id as targets_get_warehouse_row_by_id
from apps.targets.rack.api import get_rack_row_by_id as targets_get_rack_row_by_id
from apps.targets.production.api import get_production_row_by_id as targets_get_production_row_by_id
from apps.targets.customer.api import get_customer_row_by_id as targets_get_customer_row_by_id
from apps.targets.customer_contact.api import get_customer_contact_row as targets_get_customer_contact_row
from apps.targets.delivery.api import (
    count_delivery as targets_count_delivery,
    add_delivery as targets_add_delivery,
    edit_delivery as targets_edit_delivery,
)
from apps.targets.delivery_items.api import (
    count_delivery_items as targets_count_delivery_items,
    add_delivery_items as targets_add_delivery_items,
    edit_delivery_items as targets_edit_delivery_items,
)

from apps.migrations.contrast.api import (
    get_contrast_row,
    add_contrast,
)


class DeliveriesSyncResource(Resource):
    """
    DeliveriesSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/deliveries/sync
        :return:
        """
        last_pk = '00000000-0000-0000-0000-000000000000'
        limit_num = 2000

        count_add = 0           # 新增数量
        count_update = 0        # 更新数量
        count_duplicate = 0     # 重复数量

        while 1:
            delivery_rows = sources_get_delivery_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not delivery_rows:
                break
            for delivery_item in delivery_rows:

                last_pk = delivery_item.id
                source_delivery_id = delivery_item.id
                # target_delivery_id = 0

                # 获取目标
                contrast_row_delivery = get_contrast_row(table_name='delivery', pk_source=source_delivery_id)
                if contrast_row_delivery:
                    # target_delivery_id = contrast_row_delivery.pk_target
                    # 过滤重复
                    count_duplicate += 1
                    continue

                # 获取客户
                contrast_row_customer = get_contrast_row(
                    table_name='customer',
                    pk_source=delivery_item.idsettleCustomer,
                )
                if not contrast_row_customer:
                    print('customer not exist', delivery_item.idsettleCustomer)
                    continue
                target_customer_cid = contrast_row_customer.pk_target
                target_customer = targets_get_customer_row_by_id(target_customer_cid)
                if not target_customer:
                    print('customer not exist', target_customer_cid)
                    continue

                # 获取联系方式
                target_customer_contact = targets_get_customer_contact_row(
                    cid=target_customer_cid,
                    status_default=1,
                    status_delete=0,
                )
                if not target_customer_contact:
                    print('customer contact not exist', target_customer_cid)
                    continue

                # 获取制单人员
                target_user_id = 0
                contrast_row_user = get_contrast_row(
                    table_name='user',
                    pk_source=delivery_item.makerid,
                )
                if contrast_row_user:
                    target_user_id = contrast_row_user.pk_target
                else:
                    print('user not exist', delivery_item.makerid)

                # 获取审核人员
                target_audit_user_id = 0
                if delivery_item.auditorid:
                    contrast_row_auditor = get_contrast_row(
                        table_name='user',
                        pk_source=delivery_item.auditorid,
                    )
                    if contrast_row_auditor:
                        target_audit_user_id = contrast_row_auditor.pk_target
                    else:
                        print('auditor not exist', delivery_item.auditorid)

                # 获取仓库
                source_warehouse_id = delivery_item.idwarehouse
                contrast_row_warehouse = get_contrast_row(table_name='warehouse', pk_source=source_warehouse_id)
                if not contrast_row_warehouse:
                    print('warehouse not exist')
                    continue
                target_warehouse_id = contrast_row_warehouse.pk_target
                # 仓库详情
                target_warehouse = targets_get_warehouse_row_by_id(target_warehouse_id)
                if not target_warehouse:
                    print('warehouse not exist')
                    continue

                current_time = datetime.utcnow()
                # 新建（无历史导入记录）
                # if not target_delivery_id:
                delivery_data = {
                    'uid': target_user_id,
                    'customer_cid': target_customer_cid,
                    'customer_company_name': target_customer.company_name,
                    'customer_contact_id': target_customer_contact.id,
                    'type_delivery': 0,
                    'amount_production': delivery_item.taxAmount,
                    'amount_delivery': delivery_item.taxAmount,
                    'warehouse_id': target_warehouse_id,
                    'note': delivery_item.memo,
                    'type_tax': 1 if delivery_item.taxAmount > delivery_item.amount else 0,
                    'create_time': delivery_item.createdtime,
                    'update_time': delivery_item.updated,
                }
                if target_audit_user_id:
                    delivery_data['audit_uid'] = target_audit_user_id
                    delivery_data['status_audit'] = 1 if target_audit_user_id else 0
                    delivery_data['audit_time'] = delivery_item.updated

                target_delivery_id = targets_add_delivery(delivery_data)

                # 获取明细
                sources_delivery_items = sources_get_delivery_items_rows(idSaleDeliveryDTO=source_delivery_id)
                for sources_delivery_item in sources_delivery_items:
                    source_delivery_items_id = sources_delivery_item.id
                    # 获取产品
                    source_production_id = sources_delivery_item.idinventory
                    contrast_row_production = get_contrast_row(table_name='production',
                                                               pk_source=source_production_id)
                    if not contrast_row_production:
                        print('production not exist', source_production_id)
                        continue
                    target_production_id = contrast_row_production.pk_target
                    # 产品详情
                    target_production = targets_get_production_row_by_id(target_production_id)
                    if not target_production:
                        print('production not exist', target_production_id)
                        continue

                    # 获取仓位
                    target_rack_id = 0
                    source_rack_id = sources_delivery_item.inventoryLocation
                    contrast_row_rack = get_contrast_row(table_name='rack', pk_source=source_rack_id)
                    if not contrast_row_rack:
                        print('rack not exist', source_rack_id)
                    else:
                        target_rack_id = contrast_row_rack.pk_target

                    # 插入明细
                    delivery_item_data = {
                        'delivery_id': target_delivery_id,
                        'uid': target_user_id,
                        'customer_cid': target_customer_cid,
                        'customer_company_name': target_customer.company_name,
                        'production_id': target_production_id,
                        'production_brand': target_production.production_brand,
                        'production_model': target_production.production_model,
                        'production_sku': target_production.production_sku,
                        'warehouse_id': target_warehouse_id,
                        'rack_id': target_rack_id,
                        'type_tax': 1 if delivery_item.taxAmount > delivery_item.amount else 0,
                        'quantity': sources_delivery_item.quantity,
                        'unit_price': sources_delivery_item.taxPrice,
                        'create_time': delivery_item.createdtime,
                        'update_time': delivery_item.updated,
                    }
                    target_delivery_items_id = targets_add_delivery_items(delivery_item_data)
                    # 标记关系
                    contrast_data = {
                        'table_name': 'delivery_items',
                        'pk_source': source_delivery_items_id,
                        'pk_target': target_delivery_items_id,
                        'create_time': current_time,
                        'update_time': current_time,
                    }
                    add_contrast(contrast_data)

                # 标记关系
                contrast_data = {
                    'table_name': 'delivery',
                    'pk_source': source_delivery_id,
                    'pk_target': target_delivery_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                add_contrast(contrast_data)

                count_add += 1

        result = {
            '来源总数': sources_count_delivery(),
            '目标总数': targets_count_delivery(),
            '新增数量': count_add,
            '更新数量': count_update,
            '重复数量': count_duplicate,
        }

        return jsonify(result)
