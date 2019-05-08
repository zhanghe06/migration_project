#!/usr/bin/env python
# encoding: utf-8


from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from config import current_config

BASE_DIR = current_config.BASE_DIR
SQLALCHEMY_BINDS = current_config.SQLALCHEMY_BINDS


def gen_models(app_name, db_key, table_name):
    """
    创建 models 支持多库
    :param app_name:
    :param db_key:
    :param table_name:
    :return:
    """
    file_path = os.path.join(BASE_DIR, app_name, 'models', db_key, '%s.py' % table_name.lower())
    # cmd = 'sqlacodegen "%s" --noinflect --outfile %s' % (SQLALCHEMY_BINDS[db_key], file_path)
    cmd = 'sqlacodegen "%s" --noviews --noconstraints --noinflect --tables %s --outfile %s' % \
          (SQLALCHEMY_BINDS[db_key], table_name, file_path)
    print(cmd)

    output = os.popen(cmd)
    result = output.read()
    print(result)

    # 更新 model 文件
    with open(file_path, b'r') as f:
        lines = f.readlines()
    # 替换 model 关键内容
    lines[3] = b'from %s.databases.%s import db\n' % (app_name, db_key)
    lines[6] = b'Base = db.Model\n'

    # 新增 model 转 dict 方法
    with open(file_path, b'w') as f:
        lines.insert(10, b'def to_dict(self):\n')
        lines.insert(11, b'    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}\n')
        lines.insert(12, b'\n')
        lines.insert(13, b'Base.to_dict = to_dict\n')
        lines.insert(14, b'Base.__bind_key__ = \'%s\'\n' % db_key)
        lines.insert(15, b'\n\n')
        f.write(b''.join(lines))


def usage():
    print('''
创建/更新 models
$ python gen_mssql.py [项目名称] [数据库键] [数据表名]
$ python gen_mssql.py apps db_source EAP_User               # 用户
$ python gen_mssql.py apps db_source eap_Enum               # 
$ python gen_mssql.py apps db_source eap_EnumItem           # 
$ python gen_mssql.py apps db_source AA_Partner             # 往来单位
$ python gen_mssql.py apps db_source AA_Inventory           # 存货（产品）
$ python gen_mssql.py apps db_source AA_Warehouse           # 仓库
$ python gen_mssql.py apps db_source AA_InventoryLocation   # 货位
$ python gen_mssql.py apps db_source ST_CurrentStock        # 现存量
$ python gen_mssql.py apps db_source SA_SaleDelivery        # 销货单
$ python gen_mssql.py apps db_source SA_SaleDelivery_b      # 销货单明细
$ python gen_mssql.py apps db_source PU_PurchaseArrival     # 进货单
$ python gen_mssql.py apps db_source PU_PurchaseArrival_b   # 进货单明细
''')


def run():
    """
    入口
    """
    # print sys.argv
    try:
        if len(sys.argv) < 4:
            raise Exception('缺失参数\n')
        gen_models(sys.argv[1], sys.argv[2], sys.argv[3])
    except Exception as e:
        print(e.message)
        usage()


if __name__ == '__main__':
    run()
    # print(BASE_DIR)
