#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-05-08 16:32
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
# from apps.sources.apis.current_stock import (
#     get_current_stock_row_by_id as sources_get_purchase_row_by_id,
#     get_current_stock_limit_rows_by_last_id as sources_get_purchase_limit_rows_by_last_id,
#     count_current_stock as sources_count_purchase,
# )

from apps.sources.apis.purchase import (
    get_purchase_row_by_id as sources_get_purchase_row_by_id,
    get_purchase_limit_rows_by_last_id as sources_get_purchase_limit_rows_by_last_id,
    count_purchase as sources_count_purchase,
)
from apps.sources.apis.purchase_items import (
    get_purchase_items_rows as sources_get_purchase_items_rows,
    # add_purchase_items as sources_add_purchase_items,
)
from apps.targets.warehouse.api import get_warehouse_row_by_id as targets_get_warehouse_row_by_id
from apps.targets.rack.api import get_rack_row_by_id as targets_get_rack_row_by_id
from apps.targets.production.api import get_production_row_by_id as targets_get_production_row_by_id
from apps.targets.supplier.api import get_supplier_row_by_id as targets_get_supplier_row_by_id
from apps.targets.supplier_contact.api import get_supplier_contact_row as targets_get_supplier_contact_row
from apps.targets.purchase.api import (
    count_purchase as targets_count_purchase,
    add_purchase as targets_add_purchase,
    edit_purchase as targets_edit_purchase,
)
from apps.targets.purchase_items.api import (
    count_purchase_items as targets_count_purchase_items,
    add_purchase_items as targets_add_purchase_items,
    edit_purchase_items as targets_edit_purchase_items,
)

from apps.migrations.contrast.api import (
    get_contrast_row,
    add_contrast,
)

from maps.type_tax import TYPE_TAX_HAS, TYPE_TAX_NOT
from maps.type_purchase import TYPE_PURCHASE_NORMAL


class PurchasesSyncResource(Resource):
    """
    PurchasesSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/purchases/sync
        :return:
        """
        last_pk = '00000000-0000-0000-0000-000000000000'
        limit_num = 2000

        count_add = 0           # 新增数量
        count_update = 0        # 更新数量
        count_duplicate = 0     # 重复数量

        while 1:
            purchase_rows = sources_get_purchase_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not purchase_rows:
                break
            for purchase_item in purchase_rows:

                last_pk = purchase_item.id
                source_purchase_id = purchase_item.id
                # target_purchase_id = 0

                # 获取目标
                contrast_row_purchase = get_contrast_row(table_name='purchase', pk_source=source_purchase_id)
                if contrast_row_purchase:
                    # target_purchase_id = contrast_row_purchase.pk_target
                    # 过滤重复
                    count_duplicate += 1
                    continue

                # 获取渠道
                contrast_row_supplier = get_contrast_row(
                    table_name='supplier',
                    pk_source=purchase_item.idpartner,
                )
                if not contrast_row_supplier:
                    print('supplier not exist', purchase_item.idpartner)
                    continue
                target_supplier_cid = contrast_row_supplier.pk_target
                target_supplier = targets_get_supplier_row_by_id(target_supplier_cid)
                if not target_supplier:
                    print('supplier not exist', target_supplier_cid)
                    continue

                # 获取联系方式
                target_supplier_contact = targets_get_supplier_contact_row(
                    cid=target_supplier_cid,
                    status_default=1,
                    status_delete=0,
                )
                if not target_supplier_contact:
                    print('supplier contact not exist', target_supplier_cid)
                    continue

                # 获取制单人员
                target_user_id = 0
                contrast_row_user = get_contrast_row(
                    table_name='user',
                    pk_source=purchase_item.makerid,
                )
                if contrast_row_user:
                    target_user_id = contrast_row_user.pk_target
                else:
                    print('user not exist', purchase_item.makerid)

                # 获取审核人员
                target_audit_user_id = 0
                if purchase_item.auditorid:
                    contrast_row_auditor = get_contrast_row(
                        table_name='user',
                        pk_source=purchase_item.auditorid,
                    )
                    if contrast_row_auditor:
                        target_audit_user_id = contrast_row_auditor.pk_target
                    else:
                        print('auditor not exist', purchase_item.auditorid)

                # 获取仓库
                source_warehouse_id = purchase_item.idwarehouse
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
                # if not target_purchase_id:
                purchase_data = {
                    'uid': target_user_id,
                    'supplier_cid': target_supplier_cid,
                    'supplier_company_name': target_supplier.company_name,
                    'supplier_contact_id': target_supplier_contact.id,
                    'type_purchase': TYPE_PURCHASE_NORMAL,
                    'amount_production': purchase_item.totalTaxAmount,
                    'amount_purchase': purchase_item.totalTaxAmount,
                    'warehouse_id': target_warehouse_id,
                    'note': purchase_item.memo,
                    'type_tax': TYPE_TAX_HAS if purchase_item.totalTaxAmount > purchase_item.totalAmount else TYPE_TAX_NOT,
                    'create_time': purchase_item.createdtime,
                    'update_time': purchase_item.updated,
                }
                if target_audit_user_id:
                    purchase_data['audit_uid'] = target_audit_user_id
                    purchase_data['status_audit'] = 1 if target_audit_user_id else 0
                    purchase_data['audit_time'] = purchase_item.updated

                target_purchase_id = targets_add_purchase(purchase_data)

                # 获取明细
                sources_purchase_items = sources_get_purchase_items_rows(idPurchaseArrivalDTO=source_purchase_id)
                for sources_purchase_item in sources_purchase_items:
                    source_purchase_items_id = sources_purchase_item.id
                    # 获取产品
                    source_production_id = sources_purchase_item.idinventory
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
                    source_rack_id = sources_purchase_item.inventoryLocation
                    contrast_row_rack = get_contrast_row(table_name='rack', pk_source=source_rack_id)
                    if not contrast_row_rack:
                        print('rack not exist', source_rack_id)
                    else:
                        target_rack_id = contrast_row_rack.pk_target

                    # 插入明细
                    purchase_item_data = {
                        'purchase_id': target_purchase_id,
                        'uid': target_user_id,
                        'supplier_cid': target_supplier_cid,
                        'supplier_company_name': target_supplier.company_name,
                        'production_id': target_production_id,
                        'production_brand': target_production.production_brand,
                        'production_model': target_production.production_model,
                        'production_sku': target_production.production_sku,
                        'warehouse_id': target_warehouse_id,
                        'rack_id': target_rack_id,
                        'type_tax': TYPE_TAX_HAS if purchase_item.totalTaxAmount > purchase_item.totalAmount else TYPE_TAX_NOT,
                        'quantity': sources_purchase_item.quantity,
                        'unit_price': sources_purchase_item.taxPrice,
                        'create_time': purchase_item.createdtime,
                        'update_time': purchase_item.updated,
                    }
                    target_purchase_items_id = targets_add_purchase_items(purchase_item_data)
                    # 标记关系
                    contrast_data = {
                        'table_name': 'purchase_items',
                        'pk_source': source_purchase_items_id,
                        'pk_target': target_purchase_items_id,
                        'create_time': current_time,
                        'update_time': current_time,
                    }
                    add_contrast(contrast_data)

                # 标记关系
                contrast_data = {
                    'table_name': 'purchase',
                    'pk_source': source_purchase_id,
                    'pk_target': target_purchase_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                add_contrast(contrast_data)

                count_add += 1

        result = {
            '来源总数': sources_count_purchase(),
            '目标总数': targets_count_purchase(),
            '新增数量': count_add,
            '更新数量': count_update,
            '重复数量': count_duplicate,
        }

        return jsonify(result)
