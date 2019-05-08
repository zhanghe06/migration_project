# 项目迁移 - 最佳实践

**MSSqlServer** to **MariaDB**


## 项目目标
1. 前期新旧项目并行
2. 后期历史项目分离


## 项目优势
1. 使用独立迁移项目, 避免对新旧项目侵入式修改
2. 新项目独立运营时, 停止旧项目和迁移项目即可


## 项目演示
python2
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_backend.py
```


## 迁移步骤
1、清除迁移库
2、清除目标库
3、修改配置
4、执行迁移


## 服务依赖
- MariaDB
- Redis


## 项目依赖
```bash
pip install Flask-RESTful
pip install Flask-HTTPAuth
pip install Flask-SQLAlchemy
pip install sqlacodegen==1.1.6
pip install gunicorn
pip install eventlet
pip install mysqlclient
pip install cython
pip install pymssql
pip install redis
pip install requests
pip install celery
pip install grequests
```


## pymssql 安装记录
Mac 安装 freetds(pymssql的依赖)

http://pymssql.org/en/stable/freetds.html

```
brew unlink freetds
brew install freetds@0.91
brew link --overwrite --force freetds@0.91
echo 'export PATH="/usr/local/opt/freetds@0.91/bin:$PATH"' >> ~/.zshrc
```

ImportError: No module named Cython.Distutils
```
pip install cython
```


## Hack sqlacodegen 让无主键的表生成正常的model

.venv/lib/python2.7/site-packages/sqlacodegen/codegen.py
```
# Only form model classes for tables that have a primary key and are not association tables
if noclasses or not table.primary_key or table.name in association_tables:
    model = ModelTable(table)
else:
    model = ModelClass(table, links[table.name], inflect_engine, not nojoined)
    classes[model.name] = model
```
改为
```
if noclasses:
    model = ModelTable(table)
else:
    model = ModelClass(table, links[table.name], inflect_engine, not nojoined)
    classes[model.name] = model
```

```bash
cp .venv/lib/python2.7/site-packages/sqlacodegen/codegen.py .venv/lib/python2.7/site-packages/sqlacodegen/codegen.py.bak

# Linux
sed -i "s/if noclasses or not table.primary_key or table.name in association_tables:/if noclasses:/g" .venv/lib/python2.7/site-packages/sqlacodegen/codegen.py

# MacOS
sed -i "" "s/if noclasses or not table.primary_key or table.name in association_tables:/if noclasses:/g" .venv/lib/python2.7/site-packages/sqlacodegen/codegen.py
```


## ORM 主键

1. model文件中，给没有主键的表添加主键（本项目已处理, 无需重复操作）

```
基本上所有的ORM都需要主键
如果没有主键就无法定位某个table的某行row, 如果无法定位某行row, 就无法做Object-relational mapping这样的映射
一般一行row就被映射成一个Object
```

2. 处理主键名称: Id、ID、key（本项目已处理, 无需重复操作）


## 表名（T+12.0专业版）

来源表名 | 备注 | 目标表名
--- | --- | ---
EAP_User | 用户 | user
AA_Partner | 往来单位 | customer/supplier
AA_Inventory | 存货（产品） | production
ST_CurrentStock | 现存量 | inventory


## T+ 密码

密码数据库中加密存储
```
base64encode(md5('password').digest())
```

```python
#!/usr/bin/env python
# encoding: utf-8

import base64
import binascii
import hashlib

password = '123456'
password_db = '4QrcOUm6Wau+VuBX8g+IPg=='

md5 = hashlib.md5()
md5.update(password)

# md5 2进制
password_md5 = md5.digest()
print('password_md5: %s' % password_md5)

# md5 16进制
password_md5_hex = md5.hexdigest()
print('password_md5_hex: %s' % password_md5_hex)

# 2进制转16进制
password_md5_hex = binascii.b2a_hex(password_md5)
print('password_md5_hex: %s' % password_md5_hex)

# 16进制转2进制
password_md5 = binascii.a2b_hex(password_md5_hex)
print('password_md5: %s' % password_md5)

# base64 encode
password_base64_encode = base64.encodestring(password_md5)
print('password_base64_encode: %s' % password_base64_encode)

# base64 decode
password_base64_decode = base64.decodestring(password_base64_encode)
print('password_base64_decode: %s' % password_base64_decode)
```

MD5有两种表现形式:
1. hashlib.md5.digest()       # 二进制
2. hashlib.md5.hexdigest()    # 十六进制

```
password_md5: �
�9I�Y��V�W��>
password_md5_hex: e10adc3949ba59abbe56e057f20f883e
password_md5_hex: e10adc3949ba59abbe56e057f20f883e
password_md5: �
�9I�Y��V�W��>
password_base64_encode: 4QrcOUm6Wau+VuBX8g+IPg==

password_base64_decode: �
�9I�Y��V�W��>
```


## flask_restful 异常注册

flask_restful 使用 status 来处理状态

抛出自定义错误, 使用 description
```
raise TokenExpired(description=u'Token 已过期')
```

定义自定义错误
```
'TokenExpired': {
    'message': 'Token expired.',
    'status': 403,
}
```
