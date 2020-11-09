# scrapy 笔记

## 目录

- [一、中间件](#一、中间件)
    - [1.1 scrapy中间件的默认优先级](#1.1 scrapy中间件的默认优先级)
    - [1.2 retry中间件](#1.2 retry中间件)
    - [1.3 代理中间件自定义](#1.3 代理中间件自定义)
    - [1.4 添加selenium](#1.4 添加selenium)
- [二、其它](二、其它)
    - [2.1 scrapy log日志](#2.1 scrapy log日志)
    - [2.2 scrapy 执行](#2.2 scrapy 执行)
    - [2.3 scrapy-redis](#2.3 scrapy-redis)
    - [2.4 媒体文件下载](#2.4 媒体文件下载)
    - [2.5 捕获异常](#2.5 捕获异常)
    - [2.6 添加cookies三种方法](#2.6 添加cookies三种方法)
    - [2.7 发送json数据(post)](#2.7 发送json数据(post))
    - [2.8 cookiejar使用](#2.8 cookiejar使用)
    - [2.9 scrapy shell  加入ua和cookie](#2.9 scrapy shell  加入ua和cookie)
    - [2.10 优雅的导入settings的配置](#2.10 优雅的导入settings的配置)
- [声明](#声明)

## 一、中间件

### 1.1 scrapy中间件的默认优先级

```python
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
```
`process_request()` 每个中间件的方法将以**递增**的中间件顺序（100、200、300，...）`process_response()`每个中间件的方法将以**递减**(300,200,100)顺序被调用

### 1.2 retry中间件

代码1:保存信息
```python
class GetFailedUrl(RetryMiddleware):
    def __init__(self, settings):
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
        # 将爬取失败的URL存下来，你也可以存到别的存储
            with open(str(spider.name) + ".txt", "a") as f:
                f.write(response.url + "\n")
            return response
        return response

    def process_exception(self, request, exception, spider):
        # 出现异常的处理
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            with open(str(spider.name) + ".txt", "a") as f:
                f.write(str(request) + "\n")
            return None
```

代码2：重试
```python
class MyRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            time.sleep(random.randint(3, 5))
            self.logger.warning('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            time.sleep(random.randint(3, 5))
            self.logger.warning('连接异常, 保存文件后进行重试...')
            with open(str(spider.name) + ".txt", "a") as f:
                f.write(str(request) + "\n")
            return self._retry(request, exception, spider)
```

### 1.3 代理中间件自定义

代码
```python
class Proxy():
    def __init__(self):
        self.url = 'http://192.168.0.11:5010/get/'
        self.del_url = "http://192.168.0.11:5010/delete?proxy={}"
        # 网站是http的就改成http，网站是https的就改成https
        self.proxy_header = 'http://'

    def get_proxy(self):
        proxy = self.proxy_header + requests.get(self.url).json().get('proxy',False)
        return proxy

    def del_proxy(self, proxy):
        # 删除代理池的ip，慎用
        requests.get(self.del_url.format(proxy.lstrip(self.proxy_header)))

class AddProxyMiddlewares():
    def __init__(self):
        # 失效代理的集合
        self.invalid_proxy = set()
        self.proxy = Proxy().get_proxy()

    def process_request(self,request,spider):
        request.meta['HTTP_USER_AGENT'] = UserAgent().chrome
        # 清空无效代理
        if len(self.invalid_proxy) > 10:
            self.invalid_proxy.clear()
        request.meta["proxy"] = self.proxy
        logger.info('now proxy is {}'.format(self.proxy))
        return None

    def process_response(self,request,response,spider):
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            logger.warning('bad response.status {},'.format(str(response.status)))
            # 获取失效代理并收集,重新获取一个代理
            NgProxy = request.meta['proxy']
            self.invalid_proxy.add(NgProxy)
            logger.info('it is process_response invalid proxy is {},'.format(NgProxy))
            self.proxy = Proxy().get_proxy()
        return response

    def process_exception(self,request,exception,spider):
        # 进入异常模块，
        NgProxy = request.meta['proxy']
        logger.error('spider is exception, exception infomation is %s', exception)
        logger.error('this is in process_exception, invalid proxy is {},'.format(NgProxy))
        self.invalid_proxy.add(NgProxy)
```
### 1.4 添加selenium

```python

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse

logger = logging.getLogger(__name__)

class SeleniumMiddle():
    def __init__(self, timeout=10, service_args=[]):
        self.timeout = timeout
        option = webdriver.FirefoxOptions()
        option.add_argument('-headless')  # 设置option,后台运行 
        self.browser = webdriver.Firefox(firefox_options=option)
        # self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()
        
    def process_request(self, request, spider):
        """
        抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        logger.debug('Firefox is Starting')
        try:
            self.browser.get(request.url)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#test_table')))
            page_source = self.browser.page_source
            return HtmlResponse(url=request.url, body=page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=501, request=request)

```

## 二、其它

### 2.1 scrapy log日志

\# 日志文件settings.py中
```python
LOG_LEVEL= 'DEBUG'
LOG_FILE ='log.txt'
```

爬虫代码中

可以直接引用self.logger
self.logger.info(...)
但是middleware中不能直接引用,需要导入模块

默认time_out时间为180s
修改: request.meta['download_timeout']=60  (数值自己定)

### 2.2 scrapy 执行

第一种，简单，但类本身在最后一行有句sys.exit(cmd.exitcode)，注定了他执行完就退出程序，不再执行后面的语句，所以只适合调试时使用。

```python
# -*- coding:utf-8 -*-
from scrapy import cmdline
# 方式一：注意execute的参数类型为一个列表
cmdline.execute('scrapy crawl spidername'.split())
# 方式二:注意execute的参数类型为一个列表
cmdline.execute(['scrapy', 'crawl', 'spidername'])
```

第二种，相对第一种会多几行代码，但是没有第一种的缺点，建议使用。
```python
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('SpiderName', domain='123.com')
process.start() # the script will block here until the crawling is finished
```

## 2.3 scrapy-redis

### scrapy_redis

lpush [键名]:start_urls  http://youjia.chemcp.com/youjiamap.asp

添加入redis数据库 来启动redis

### settings.py中设置

```python
# 启动scrapy-redis引擎
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 共享筛选器
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 不清空爬虫队列
SCHEDULER_PERSIST = True
# 使用优先级队列调度
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
'scrapy_redis.pipelines.RedisPipeline': 300,

REDIE_URL = None
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
```

### 2.4 媒体文件下载

file示例
#### settings.py

\# 文件下载路径
FILES_STORE = 'D:\\result'

#### pipeline
```python
class MyFilePipeline(FilesPipeline):

    def get_media_requests(self, item,info):

        yield scrapy.Request(item['content_url'])

    def file_path(self, request, response=None, info=None):
        """
        重命名模块
        """
        path = os.path.join(FILES_STORE, request.url[-10:])

        logger.info("file_path:{}".format(request.url[-10:]))

        return path
```

### 2.5 捕获异常

```python
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
 
class ProcessAllExceptionMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)
    def process_response(self,request,response,spider):
        #捕获状态码为40x/50x的response
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            #随意封装，直接返回response，spider代码中根据url==''来处理response
            response = HtmlResponse(url='')
            return response
        #其他状态码不处理
        return response
    def process_exception(self,request,exception,spider):
        #捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            #在日志中打印异常类型
            print('Got exception: %s' % (exception))
            #随意封装一个response，返回给spider
            response = HtmlResponse(url='exception')
            return response
        #打印出未捕获到的异常
        print('not contained exception: %s'%exception)
```

### 2.6 添加cookies三种方法

1.settings
settings文件中给Cookies_enabled=False解注释
settings的headers配置的cookie就可以用了
这种方法最简单，同时cookie可以直接粘贴浏览器的。
后两种方法添加的cookie是字典格式的，需要用json反序列化一下,
而且需要设置settings中的Cookies_enabled=True

2.DownloadMiddleware
settings中给downloadmiddleware解注释
去中间件文件中找downloadmiddleware这个类，修改process_request，添加request.cookies={}即可。

3.爬虫主文件中重写start_request

```python
def start_requests(self):
    yield scrapy.Request(url,dont_filter=True,cookies={自己的cookie})
```

### 2.7 发送json数据(post)

scrapy Post 发送数据是我们通常会用
```python
yield scrapy.FormRequest(
            url = url,
            formdata = {"email" : "xxx", "password" : "xxxxx"},
            callback = self.parse_page
        )
```
来发送请求，但这是发送header为

`'Content-Type', 'application/x-www-form-urlencoded'`
的数据，有时候我们做一些爬虫，会post发送json数据，否则不能返回正确的结果，如果直接用request很方便，但在scrapy里就需要这样用
```python
yield Request(url, method="POST", body=json.dumps(data), headers={'Content-Type': 'application/json'},callback=self.parse_json)
```
这样就可以发送json 数据了

### 2.8 cookiejar使用

**meta当然是可以传递cookie的（第一种）：**

下面start_requests中键‘cookiejar’是一个特殊的键，scrapy在meta中见到此键后，会自动将cookie传递到要callback的函数中。既然是键(key)，就需要有值(value)与之对应，例子中给了数字1，也可以是其他值，比如任意一个字符串。

```python
def start_requests(self):
    yield Request(url,meta={'cookiejar':1},callback=self.parse)
```

需要说明的是，meta给‘cookiejar’赋值除了可以表明要把cookie传递下去，还可以对cookie做标记。一个cookie表示一个会话(session)，如果需要经多个会话对某网站进行爬取，可以对cookie做标记，1,2,3,4......这样scrapy就维持了多个会话。

```python
def parse(self,response):
    key=response.meta['cookiejar']    #经过此操作后，key=1
    yield Request(url2,meta={'cookiejar'：key},callback='parse2')
def parse2(self,response):
    pass
```

上面这段和下面这段是等效的：

```python
def parse(self,response):
    yield Request(url2,meta={'cookiejar'：response.meta['cookiejar']},callback='parse2')
    #这样cookiejar的标记符还是数字1
def parse2(self,response):
    pass
```

**传递cookie的第二种写法：**

如果不加标记，可以用下面的写法：

```python
#先引入CookieJar()方法
from scrapy.http.cookies import CookieJar
```

写spider方法时：

```python
def start_requests(self):
    yield Request(url,callback=self.parse)#此处写self.parse或‘parse’都可以
def parse(self,response):
    cj = response.meta.setdefault('cookie_jar', CookieJar())
    cj.extract_cookies(response, response.request)
    container = cj._cookies
    yield Request(url2,cookies=container,meta={'key':container},callback='parse2')
def parse2(self,response):
    pass
```



**meta是浅复制，必要时需要深复制。**

可以这样引入：

```python
import copy
meta={'key':copy.deepcopy('value')}
```

### 2.9 scrapy shell  加入ua和cookie

`scrapy shell 'https://www.qq.com/' -s USER_AGENT='(Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'`

\# 指定请求目标的 URL 链接

url_ = 'https://www.google.com'

\# 自定义 Headers 请求头(一般建议在调试时使用自定义 UA，以绕过最基础的 User-Agent 检测)

headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}

\# 构造需要附带的 Cookies 字典

cookies_ = {"key_1": "value_1", "key_2": "value_2", "key_3": "value_3"}

\# 构造 Request 请求对象

req = scrapy.Request(url_, cookies=cookies_, headers=headers_)

\# 发起 Request 请求

fetch(req)

\# 在系统默认浏览器查看请求的页面（主要为了检查是否正常爬取到内页）

view(response)

### 2.10 优雅的导入settings的配置

scrapy提供了导入设置的方法：from_crawler

```python
@classmethod
def from_crawler(cls, crawler):
  server = crawler.settings.get('SERVER')
  # FIXME: for now, stats are only supported from this constructor
  return cls(server)
```

接着，只要在__init__接收这些参数就可以了。

```python
def __init__(self, server):
	self.server = server
```

而在一些官方的组件的源码中会这样使用，不过这看起来有点多此一举

```python
@classmethod
def from_settings(cls, settings):
	server = settings.get('SERVER')
	return cls(server)

@classmethod
def from_crawler(cls, crawler):
  # FIXME: for now, stats are only supported from this constructor
  return cls.from_settings(crawler.settings)
```

另外，并不是所有的类都可以使用这个类方法。只有像**插件,中间件,信号管理器和项目管道**等这些组件才能使用这个类方法来导入配置，如果是自己写的spider或者自定义文件并没有，需要使用如下方法导入：

```python
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
```

这里的settings就是包含settings.py的所有配置的字典了。

## 声明

内容基本上来源于网络，仅提供参考作用，**需自己验证**