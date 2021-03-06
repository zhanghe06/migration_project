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
```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_apps.py
```

```bash
python tasks/task_token.py
```

[http://0.0.0.0:8000](http://0.0.0.0:8000)


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
pip install schedule
pip install future
pip install supervisor
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
AA_Warehouse | 仓库 | warehouse
AA_InventoryLocation | 货位 | rack
ST_CurrentStock | 现存量 | inventory
SA_SaleDelivery | 销货单 | delivery
SA_SaleDelivery_b | 销货单明细 | delivery_items
PU_PurchaseArrival | 进货单 | purchase
PU_PurchaseArrival_b | 进货单明细 | purchase_items


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

## SSH Tunnel

开启隧道
```bash
sh ssh_tunnel/start_default.sh
```
这里将远程3306端口映射为本地3366端口

修改配置
```
# 数据库 端口 3306 > 3366
DB_MYSQL_TARGET = {
    'host': HOST,
    'user': 'root',
    'passwd': '123456',
    'port': 3366,
    'db': 'db_target'
}
```

## DataGrip Use SSH Tunnel

General
```
Host        127.0.0.1
Port        3306
User        root
Password    123456
```

SSH
```
Proxy host          192.168.1.100
Port                22
Proxy user          root
Auth type           Key pair(OpenSSH)
Private key file    ~/.ssh/id_rsa
Passphrase          123456
```

## Supervisor

http://www.supervisord.org


## GoProxy

https://github.com/snail007/goproxy

https://github.com/snail007/goproxy/blob/master/README_ZH.md

背景:

公司机器A提供了web服务80端口  
有VPS一个，公网IP:22.22.22.22

需求:

在家里能够通过访问VPS的28080端口访问到公司机器A的80端口

步骤:

在vps上执行
```
./proxy bridge -p ":33080" -C proxy.crt -K proxy.key
./proxy server -r ":28080@:80" -P "127.0.0.1:33080" -C proxy.crt -K proxy.key
```

在公司机器A上面执行
```
./proxy client -P "22.22.22.22:33080" -C proxy.crt -K proxy.key
```


## schedule

https://github.com/dbader/schedule/

https://schedule.readthedocs.io/


## 数据库连接最佳实践

- 脚本应用
```python
from apps.databases.db_migration import get_migration_db
from apps.databases.db_source import get_source_db
from apps.databases.db_target import get_target_db

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.eap_user import EAPUser as SourceUser
from apps.models.db_target import User as TargetUser

from libs.db_orm_api import DbApi

migration_contrast_api = DbApi(get_migration_db(), MigrationContrast)
source_user_api = DbApi(get_source_db(), SourceUser)
target_user_api = DbApi(get_target_db(), TargetUser)
```
单独开启连接

- 网页应用
```python
from apps.databases.db_migration import migration_db
from apps.databases.db_source import source_db
from apps.databases.db_target import target_db

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.eap_user import EAPUser as SourceUser
from apps.models.db_target import User as TargetUser

from libs.db_orm_api import DbApi

migration_contrast_api = DbApi(migration_db, MigrationContrast)
source_user_api = DbApi(source_db, SourceUser)
target_user_api = DbApi(target_db, TargetUser)
```
可共用连接池


## 项目核心

文件`libs/migration_client.py`中的类：[`MigrationClient`](libs/migration_client.py)
