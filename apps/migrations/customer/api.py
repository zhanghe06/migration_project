#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-09-07 18:51
"""

from __future__ import unicode_literals

from datetime import datetime

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.aa_partner import AAPartner as SourceCustomer
from apps.models.db_target import Customer as TargetCustomer
from apps.models.db_target import CustomerContact as TargetCustomerContact
from libs.migration_client import MigrationClient
from tools.date_time import time_local_to_utc


def sync():
    customer_client = MigrationClient(
        'customer',
        SourceCustomer,
        TargetCustomer,
        MigrationContrast,
    )
    customer_contact_client = MigrationClient(
        'customer_contact',
        t_model=TargetCustomerContact,
    )

    while 1:
        s_rows = customer_client.s_api.get_limit_rows_by_last_id(
            last_pk=customer_client.s_id,
            limit_num=customer_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            customer_client.s_data = s_data
            customer_client.s_id = customer_client.s_data.id
            customer_client.latest_time = time_local_to_utc(customer_client.s_data.updated)

            # ----------
            # 往来单位性质（[eap_EnumItem]）
            # {{endpoint}}/sources/enum_items?page=1&per_page=20000&id_enum=165e3c70-718a-4938-8ca7-01bcaa30b814
            # 0c90a0c3-960d-493a-869d-72d97189e4fc 客户
            # 8e849744-d6f6-4a46-9428-7b438df6be54 供应商
            # 45a62402-6aaf-42de-9a27-7ba96b9b9d2c 客户/供应商
            partner_type_customer = ['0c90a0c3-960d-493a-869d-72d97189e4fc', '45a62402-6aaf-42de-9a27-7ba96b9b9d2c']
            partner_type = str(customer_client.s_data.partnerType)  # UUID 转 str
            # 类型判断
            if partner_type not in partner_type_customer:
                continue
            # ----------

            customer_client.m_detail()
            # 存在历史数据
            if customer_client.m_data:
                if not customer_client.s_data.updated:
                    continue
                if customer_client.latest_time <= customer_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                customer_client.t_id = customer_client.m_data.pk_target
                # 提取基本数据
                company_name = customer_client.s_data.name.strip() if customer_client.s_data.name else ''
                company_address = customer_client.s_data.ShipmentAddress.strip() if customer_client.s_data.ShipmentAddress else ''
                company_tel = customer_client.s_data.TelephoneNo.strip() if customer_client.s_data.TelephoneNo else ''
                company_fax = customer_client.s_data.Fax.strip() if customer_client.s_data.Fax else ''
                # owner_uid = customer_client.s_data.idsaleman  # todo
                customer_client.t_data = {
                    'company_name': company_name,
                    'company_address': company_address,
                    # 'company_site': '',
                    'company_tel': company_tel,
                    'company_fax': company_fax,
                    # 'company_email': '',
                    # 'company_type': '',
                    # 'owner_uid': owner_uid,
                    'update_time': current_time,
                }
                # 删除条件
                if customer_client.s_data.disabled:
                    customer_client.t_data['status_delete'] = True
                    customer_client.t_data['delete_time'] = current_time
                # ----------
                customer_client.t_update()
                # ----------
                # 更新关联数据
                t_data_customer_contact = customer_contact_client.t_api.get_row(cid=customer_client.t_id)
                if not t_data_customer_contact:
                    continue
                customer_contact_data = {
                    'cid': customer_client.t_id,
                    'name': customer_client.s_data.Contact.strip() if customer_client.s_data.Contact else '',
                    'mobile': customer_client.s_data.TelephoneNo.strip() if customer_client.s_data.TelephoneNo else '',
                    'address': customer_client.s_data.ShipmentAddress.strip() if customer_client.s_data.ShipmentAddress else '',
                    # 'status_default': True,
                }
                customer_contact_client.t_api.edit(t_data_customer_contact.id, customer_contact_data)
                # ----------
                customer_client.m_update()
            # 没有历史数据
            else:
                # 目标数据去重
                customer_client.t_data = customer_client.t_api.get_row(company_name=customer_client.s_data.name.strip())
                if customer_client.t_data:
                    continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                # 提取基本数据
                company_name = customer_client.s_data.name.strip() if customer_client.s_data.name else ''
                company_address = customer_client.s_data.ShipmentAddress.strip() if customer_client.s_data.ShipmentAddress else ''
                company_tel = customer_client.s_data.TelephoneNo.strip() if customer_client.s_data.TelephoneNo else ''
                company_fax = customer_client.s_data.Fax.strip() if customer_client.s_data.Fax else ''
                # owner_uid = customer_client.s_data.idsaleman  # todo
                customer_client.t_data = {
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
                # 删除条件
                if customer_client.s_data.disabled:
                    customer_client.t_data['status_delete'] = True
                    customer_client.t_data['delete_time'] = current_time
                # ----------
                customer_client.t_create()
                # ----------
                # 创建关联数据
                customer_contact_data = {
                    'cid': customer_client.t_id,
                    'name': customer_client.s_data.Contact.strip() if customer_client.s_data.Contact else '',
                    'mobile': customer_client.s_data.TelephoneNo.strip() if customer_client.s_data.TelephoneNo else '',
                    'address': customer_client.s_data.ShipmentAddress.strip() if customer_client.s_data.ShipmentAddress else '',
                    'status_default': True,
                }
                customer_contact_client.t_api.add(customer_contact_data)
                # ----------
                customer_client.m_create()
    result = {
        '来源总数': customer_client.s_api.count(),
        '目标总数': customer_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
