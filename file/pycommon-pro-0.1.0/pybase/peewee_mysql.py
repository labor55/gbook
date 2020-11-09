# -*- coding: utf-8 -*-
from peewee import *
from scrapy.utils.project import get_project_settings
import logging
setting = get_project_settings()
apollo_settings = {}
MYSQL_TABLE = apollo_settings.get('MYSQL_TABLE', 'ps_c23_data')
MYSQL_CLIENT = {
    'host': apollo_settings.get('MYSQL_HOST', '192.168.0.27'),
    'port': apollo_settings.get('MYSQL_PORT', 3306),
    'user': apollo_settings.get('MYSQL_USER', 'root'),
    'password': str(apollo_settings.get('MYSQL_PWD', 'lab123456')),
    'database': apollo_settings.get('MYSQL_DB', 'test'),
}

databases = MySQLDatabase(**MYSQL_CLIENT)


class Peewee(Model):
    menu_id = CharField(unique=True)
    name = CharField()
    parent_menu_id = CharField()
    seq = IntegerField(default=0)
    path = CharField()

    class Meta:
        logging.getLogger(__name__).info(">>>>>>>>>>>>>>>>>>>>>>>>>  peewee table init.............................")

        table_name = MYSQL_TABLE
        database = databases


