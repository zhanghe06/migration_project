#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2019-04-25 18:10
"""


from flask import Flask

from config import current_config

from apps.tokens.blueprints import tokens_bp
from apps.sources.blueprints import sources_bp
from apps.targets.blueprints import targets_bp
from apps.migrations.blueprints import migrations_bp


app = Flask(__name__)

# Load Config
app.config.from_object(current_config)

# Register Blueprint
app.register_blueprint(tokens_bp)
app.register_blueprint(sources_bp)
app.register_blueprint(targets_bp)
app.register_blueprint(migrations_bp)

# Add Resource Urls
# 注意顺序, 避免循环导入
from apps import urls

from apps.tokens import urls
from apps.migrations.user import urls
from apps.migrations.production import urls
from apps.migrations.inventory import urls
from apps.migrations.customer import urls
from apps.migrations.supplier import urls
from apps.migrations.warehouse import urls
from apps.migrations.rack import urls
from apps.migrations.delivery import urls
from apps.migrations.purchase import urls

from apps.sources.urls.current_stock import *
from apps.sources.urls.enum import *
from apps.sources.urls.enum_items import *
from apps.sources.urls.inventory import *
from apps.sources.urls.user import *

from apps.targets.user import urls
from apps.targets.inventory import urls


