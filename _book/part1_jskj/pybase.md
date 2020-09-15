# pybase

## 1、介绍与安装

Pybase提供了一些公用方法，是一个工具包。

下载：[点击这里](../file/pycommon-pro-0.0.9.tar.gz)

安装：`pip install pycommon-pro-0.0.9.tar.gz`

pybase包含一些工具类

- 生成parent_id
- 集成了代理添加功能
- 添加公用管道
- 文件上传接口


## 2、用法介绍

### 2.1 生成parent_id工具类

1. Settings添加配置，可以设置在Apollo中

```python
# Settings添加配置
G_ROOT_ID = 行业的分配id
G_ROOT_NAME = 行业名称
G_TABLE_NAME = 菜单的数据表的名称
MYSQL_HOST = 192.168.0.11
MYSQL_PORT = 3306
MYSQL_DATABASE = ''
MYSQL_USER = ''
MYSQL_PASSWORD = ''
```

2. Pybase模块中新增了一个自动生成工具类的工具，使用以下代码使用

```python
from pybase.MenuIdGenerator import MenuIdGenerator

class XXX():
    # 初始化
    def __init__(self):
        self.generator = MenuIdGenerator()
    # 使用
    def xxl(self):
        Item[‘parent_menu_id’] = self.generator.getMenuId(['制造业', '酒、饮料和精制茶制造业', 'xxxx'])
```

getMenuId方法返回菜单最后一级id，设置成当前数据的parent_menu_id就行了。。。。

### 2.2 添加代理功能

Pybase 模块中添加了公用的代理功能：

Settings中添加配置：

```python
# 设置代理网址
PROXY_GET_URL='http://192.168.3.85:5010/get/'
# 开启代理中间件
DOWNLOADER_MIDDLEWARES = {
    'pybase.middlewares.AddProxyMiddlewares': 543,
    'pybase.middlewares.MyRetryMiddleware': 534,
}
```

添加完成即可请求时自动添加代理功能。当然了这两个配置都可以放在apollo中。

### 2.3 添加公用管道

Pybase模块中添加了公用管道功能：

用法如下

```python
# Settings中添加配置：
MONGO_HOST = '192.168.0.22'
MONGO_PORT = '27017'
MONGO_DATABASE = 'industry'
MONGO_TABLE = 'C16_data'
MONGO_USER = ''
MONGO_PASSWORD = ''
```

如果是数据管道(根据parent_id, data_value, frequency, create_time去重)，还需要在settings中开启：

```python
ITEM_PIPELINES = {
    'pybase.pipelines.ScrapyDataPipeline': 300,
}
```

如果是资讯管道(根据news_id去重)，需要开启：

```python
ITEM_PIPELINES = {
    'pybase.pipelines.ScrapyInfoPipeline': 300,
}
```

如果是报告管道(根据content_id去重)：

```python
ITEM_PIPELINES = {
    'pybase.pipelines.ScrapyReportPipeline': 300,
}
```

### 2.4 文件上传功能

Pybase中添加了公用文件上传功能：

用法如下

```python
from pybase.util import send_file
send_file("ppp.jpg", 'https://img.chihuogu.com/file/mstj/20200807/c7.jpg', "http://192.168.3.85:8500/file/upload/spidername")
```

send_file参数解释：

> :param file_name：文件的名称
> :param file_url：文件的url
> :param upload_url: 上传文件的接口(服务器上)
> :param headers: 图片下载的headers 

Send_file方法添加失败重试功能，重试三次