#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-04-27 23:33
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
from apps.models.db_source.aa_partner import AAPartner
from apps.sources.apis.partner import (
    get_partner_limit_rows_by_last_id,
    count_partner)
from apps.targets.customer.api import count_customer, add_customer
from apps.targets.customer_contact.api import add_customer_contact
from apps.migrations.contrast.api import get_contrast_row, add_contrast


class CustomersSyncResource(Resource):
    """
    CustomersSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/customers/sync
        :return:
        """
        last_pk = '00000000-0000-0000-0000-000000000000'
        limit_num = 2000

        count_duplicate_customer = 0

        # 往来单位性质（[eap_EnumItem]）
        # {{endpoint}}/sources/enum_items?page=1&per_page=20000&id_enum=165e3c70-718a-4938-8ca7-01bcaa30b814
        # 0c90a0c3-960d-493a-869d-72d97189e4fc 客户
        # 8e849744-d6f6-4a46-9428-7b438df6be54 供应商
        # 45a62402-6aaf-42de-9a27-7ba96b9b9d2c 客户/供应商
        partner_type_customer = ['0c90a0c3-960d-493a-869d-72d97189e4fc', '45a62402-6aaf-42de-9a27-7ba96b9b9d2c']

        while 1:
            partner_rows = get_partner_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not partner_rows:
                break
            for partner_item in partner_rows:

                last_pk = partner_item.id
                source_customer_id = partner_item.id
                # source_user_id = partner_item.idsaleman

                company_name = partner_item.name.strip() if partner_item.name else ''
                company_address = partner_item.ShipmentAddress.strip() if partner_item.ShipmentAddress else ''
                company_tel = partner_item.TelephoneNo.strip() if partner_item.TelephoneNo else ''
                company_fax = partner_item.Fax.strip() if partner_item.Fax else ''
                # owner_uid = partner_item.idsaleman  # todo

                partner_type = str(partner_item.partnerType)  # UUID 转 str

                # 客户判断
                if partner_type not in partner_type_customer:
                    continue
                # 判断重复
                count_dup = count_customer(company_name=company_name)
                if count_dup:
                    count_duplicate_customer += 1
                    print(company_name)
                    print(count_duplicate_customer)
                    continue
                current_time = datetime.utcnow()

                # contrast_row_user = get_contrast_row(table_name='user', pk_source=source_user_id)
                # if not contrast_row_user:
                #     print('user not exist')
                #     continue
                # target_user_id = contrast_row_user.pk_target

                customer_data = {
                    'company_name': company_name,
                    'company_address': company_address,
                    # 'company_site': '',
                    'company_tel': company_tel,
                    'company_fax': company_fax,
                    # 'company_email': '',
                    # 'company_type': '',
                    # 'owner_uid': target_user_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                cid = add_customer(customer_data)
                target_customer_id = cid

                # 插入联系方式（默认）
                customer_contact_data = {
                    'cid': cid,
                    'name': partner_item.Contact.strip() if partner_item.Contact else '',
                    'mobile': partner_item.TelephoneNo.strip() if partner_item.TelephoneNo else '',
                    'address': partner_item.ShipmentAddress.strip() if partner_item.ShipmentAddress else '',
                    'status_default': True,
                }
                add_customer_contact(customer_contact_data)

                # 标记关系
                contrast_data = {
                    'table_name': 'customer',
                    'pk_source': source_customer_id,
                    'pk_target': target_customer_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                add_contrast(contrast_data)

        result = {
            '公司总数': count_partner(),
            '客户总数': count_partner(AAPartner.partnerType.in_(partner_type_customer)),
            '客户过滤重复': count_duplicate_customer,
            '客户成功导入': count_customer(),
        }

        return jsonify(result)
