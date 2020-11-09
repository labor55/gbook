# encoding: utf-8
"""
爬虫 常用工具包
0.0.4  修复了logger日志异常问题
0.0.5  添加ApolloSpiderConfig单例模式,,,,部分人使用出现DNS lookup 错误，，将client.start()改成同步模式
0.0.6  优化逻辑,添加将字符串数字，bool，json转化为对应类型的功能
0.0.7  添加了公用管道功能
0.0.8  添加了公用代理功能, 公用图片上传功能, 修改部分逻辑
0.0.9  移除了对apollo的支持，将apollo移动到了scrapy-2.2.1-apollo版本框架中
0.1.0  更改了自动生成菜单id的逻辑
"""
from setuptools import setup


setup(
    name='pycommon-pro',
    version='0.1.0',
    author='pengsiqi',
    author_email='',
    install_requires=['requests', 'eventlet', 'peewee', 'tenacity'],
    py_modules=[
                'pybase.apollo_setting',
                'pybase.peewee_mysql',
                'pybase.MenuIdGenerator',
                'pybase.pipelines',
                'pybase.middlewares',
                'pybase.util'
    ]
)
