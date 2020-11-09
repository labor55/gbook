# -*- coding: utf-8 -*-

from .apollo_setting import get_project_settings
from .peewee_mysql import Peewee
from .MenuIdGenerator import MenuIdGenerator
from .pipelines import ScrapyDataPipeline, ScrapyInfoPipeline, ScrapyReportPipeline
from .middlewares import Proxy, AddProxyMiddlewares, MyRetryMiddleware
from .util import send_file

__version__ = "0.1.0.dev1"
__author__ = 'pengsiqi'
__email__ = ''
