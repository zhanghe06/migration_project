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
from apps.models.db_source.aa_partner import AAPartner as SourceSupplier
from apps.models.db_target import Supplier as TargetSupplier
from apps.models.db_target import SupplierContact as TargetSupplierContact
from libs.migration_client import MigrationClient
from tools.date_time import time_local_to_utc


def sync():
    supplier_client = MigrationClient(
        'supplier',
        SourceSupplier,
        TargetSupplier,
        MigrationContrast,
    )
    supplier_contact_client = MigrationClient(
        'supplier_contact',
        SourceSupplier,
        TargetSupplierContact,
        MigrationContrast,
    )

    while 1:
        s_rows = supplier_client.s_api.get_limit_rows_by_last_id(
            last_pk=supplier_client.s_id,
            limit_num=supplier_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            supplier_client.s_data = s_data
            supplier_client.s_id = supplier_client.s_data.id
            supplier_client.latest_time = time_local_to_utc(supplier_client.s_data.updated)

            # ----------
            # 往来单位性质（[eap_EnumItem]）
            # {{endpoint}}/sources/enum_items?page=1&per_page=20000&id_enum=165e3c70-718a-4938-8ca7-01bcaa30b814
            # 0c90a0c3-960d-493a-869d-72d97189e4fc 客户
            # 8e849744-d6f6-4a46-9428-7b438df6be54 供应商
            # 45a62402-6aaf-42de-9a27-7ba96b9b9d2c 客户/供应商
            partner_type_supplier = ['8e849744-d6f6-4a46-9428-7b438df6be54', '45a62402-6aaf-42de-9a27-7ba96b9b9d2c']
            partner_type = str(supplier_client.s_data.partnerType)  # UUID 转 str
            # 类型判断
            if partner_type not in partner_type_supplier:
                continue
            # ----------

            supplier_client.m_detail()
            # 存在历史数据
            if supplier_client.m_data:
                if not supplier_client.s_data.updated:
                    continue
                if supplier_client.latest_time <= supplier_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                supplier_client.t_id = supplier_client.m_data.pk_target
                current_time = datetime.utcnow()
                # 提取基本数据
                company_name = supplier_client.s_data.name.strip() if supplier_client.s_data.name else ''
                company_address = supplier_client.s_data.ShipmentAddress.strip() if supplier_client.s_data.ShipmentAddress else ''
                company_tel = supplier_client.s_data.TelephoneNo.strip() if supplier_client.s_data.TelephoneNo else ''
                company_fax = supplier_client.s_data.Fax.strip() if supplier_client.s_data.Fax else ''
                # owner_uid = supplier_client.s_data.idsaleman  # todo
                supplier_client.t_data = {
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
                if supplier_client.s_data.disabled:
                    supplier_client.t_data['status_delete'] = True
                    supplier_client.t_data['delete_time'] = current_time
                # ----------
                supplier_client.t_update()
                # ----------
                # 更新关联数据
                t_data_supplier_contact = supplier_contact_client.t_api.get_row(cid=supplier_client.t_id)
                if not t_data_supplier_contact:
                    continue
                supplier_contact_data = {
                    'cid': supplier_client.t_id,
                    'name': supplier_client.s_data.Contact.strip() if supplier_client.s_data.Contact else '',
                    'mobile': supplier_client.s_data.TelephoneNo.strip() if supplier_client.s_data.TelephoneNo else '',
                    'address': supplier_client.s_data.ShipmentAddress.strip() if supplier_client.s_data.ShipmentAddress else '',
                    # 'status_default': True,
                }
                supplier_contact_client.t_api.edit(t_data_supplier_contact.id, supplier_contact_data)
                # ----------
                supplier_client.m_update()
            # 没有历史数据
            else:
                # 目标数据去重
                supplier_client.t_data = supplier_client.t_api.get_row(company_name=supplier_client.s_data.name.strip())
                if supplier_client.t_data:
                    continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                # 提取基本数据
                company_name = supplier_client.s_data.name.strip() if supplier_client.s_data.name else ''
                company_address = supplier_client.s_data.ShipmentAddress.strip() if supplier_client.s_data.ShipmentAddress else ''
                company_tel = supplier_client.s_data.TelephoneNo.strip() if supplier_client.s_data.TelephoneNo else ''
                company_fax = supplier_client.s_data.Fax.strip() if supplier_client.s_data.Fax else ''
                # owner_uid = supplier_client.s_data.idsaleman  # todo
                supplier_client.t_data = {
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
                if supplier_client.s_data.disabled:
                    supplier_client.t_data['status_delete'] = True
                    supplier_client.t_data['delete_time'] = current_time
                # ----------
                supplier_client.t_create()
                # ----------
                # 创建关联数据
                supplier_contact_data = {
                    'cid': supplier_client.t_id,
                    'name': supplier_client.s_data.Contact.strip() if supplier_client.s_data.Contact else '',
                    'mobile': supplier_client.s_data.TelephoneNo.strip() if supplier_client.s_data.TelephoneNo else '',
                    'address': supplier_client.s_data.ShipmentAddress.strip() if supplier_client.s_data.ShipmentAddress else '',
                    'status_default': True,
                }
                supplier_contact_client.t_api.add(supplier_contact_data)
                # ----------
                supplier_client.m_create()
    result = {
        '来源总数': supplier_client.s_api.count(),
        '目标总数': supplier_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
