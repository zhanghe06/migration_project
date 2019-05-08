#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-04-27 23:47
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
from apps.migrations.contrast.api import add_contrast
from apps.models.db_source.aa_partner import AAPartner
from apps.sources.apis.partner import (
    get_partner_limit_rows_by_last_id,
    count_partner)
from apps.targets.supplier.api import count_supplier, add_supplier
from apps.targets.supplier_contact.api import add_supplier_contact


class SuppliersSyncResource(Resource):
    """
    SuppliersSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/suppliers/sync
        :return:
        """
        last_pk = '00000000-0000-0000-0000-000000000000'
        limit_num = 2000

        count_duplicate_supplier = 0

        # 往来单位性质（[eap_EnumItem]）
        # {{endpoint}}/sources/enum_items?page=1&per_page=20000&id_enum=165e3c70-718a-4938-8ca7-01bcaa30b814
        # 0c90a0c3-960d-493a-869d-72d97189e4fc 客户
        # 8e849744-d6f6-4a46-9428-7b438df6be54 供应商
        # 45a62402-6aaf-42de-9a27-7ba96b9b9d2c 客户/供应商
        partner_type_supplier = ['8e849744-d6f6-4a46-9428-7b438df6be54', '45a62402-6aaf-42de-9a27-7ba96b9b9d2c']

        while 1:
            partner_rows = get_partner_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not partner_rows:
                break
            for partner_item in partner_rows:

                last_pk = partner_item.id
                source_supplier_id = partner_item.id

                company_name = partner_item.name.strip() if partner_item.name else ''
                company_address = partner_item.ShipmentAddress.strip() if partner_item.ShipmentAddress else ''
                company_tel = partner_item.TelephoneNo.strip() if partner_item.TelephoneNo else ''
                company_fax = partner_item.Fax.strip() if partner_item.Fax else ''
                # owner_uid = partner_item.idsaleman  # todo

                partner_type = str(partner_item.partnerType)  # UUID 转 str

                # 友商判断
                if partner_type not in partner_type_supplier:
                    continue
                # 判断重复
                count_dup = count_supplier(company_name=company_name)
                if count_dup:
                    count_duplicate_supplier += 1
                    print(company_name)
                    print(count_duplicate_supplier)
                    continue
                current_time = datetime.utcnow()

                supplier_data = {
                    'company_name': company_name,
                    'company_address': company_address,
                    # 'company_site': '',
                    'company_tel': company_tel,
                    'company_fax': company_fax,
                    # 'company_email': '',
                    # 'company_type': '',
                    # 'owner_uid': owner_uid,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                cid = add_supplier(supplier_data)
                target_supplier_id = cid

                # 插入联系方式（默认）
                supplier_contact_data = {
                    'cid': cid,
                    'name': partner_item.Contact.strip() if partner_item.Contact else '',
                    'mobile': partner_item.TelephoneNo.strip() if partner_item.TelephoneNo else '',
                    'address': partner_item.ShipmentAddress.strip() if partner_item.ShipmentAddress else '',
                    'status_default': True,
                }
                add_supplier_contact(supplier_contact_data)

                # 标记关系
                contrast_data = {
                    'table_name': 'supplier',
                    'pk_source': source_supplier_id,
                    'pk_target': target_supplier_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                add_contrast(contrast_data)

        result = {
            '公司总数': count_partner(),
            '渠道总数': count_partner(AAPartner.partnerType.in_(partner_type_supplier)),
            '渠道过滤重复': count_duplicate_supplier,
            '渠道成功导入': count_supplier(),
        }

        return jsonify(result)
