# -*- coding: utf-8 -*-
import logging
import requests
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from twisted.internet.error import TimeoutError, ConnectionRefusedError
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)


class Proxy():
    def __init__(self):
        config = get_project_settings()
        self.url = config.get('PROXY_GET_URL')

    def get_proxy(self):
        try:
            proxy = requests.get(self.url).json().get('proxy', False)
        except:
            proxy = None
        return proxy


class AddProxyMiddlewares():
    def __init__(self):
        # 失效代理的集合
        self.invalid_proxy = set()
        self.proxy = Proxy().get_proxy()

    def process_request(self, request, spider):
        # 清空无效代理
        if len(self.invalid_proxy) > 10:
            self.invalid_proxy.clear()
        if self.proxy:
            request.meta["proxy"] = ('https://' + self.proxy) if request.url.startswith('https') else (
                    'http://' + self.proxy)
            logger.debug('当前代理 ' + request.meta["proxy"])
        else:
            logger.info('代理获取失败')
        return None

    def process_response(self, request, response, spider):
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            if 'proxy' in dict(request.meta).keys():
                # 获取失效代理并收集,重新获取一个代理
                NgProxy = request.meta['proxy']
                self.invalid_proxy.add(NgProxy)
            self.proxy = Proxy().get_proxy()
            logger.info('代理中间件响应报错，状态码为{} ，新的代理为 {}'.format(str(response.status), self.proxy))
        return response

    def process_exception(self, request, exception, spider):
        # 进入异常模块，
        if 'proxy' in dict(request.meta).keys():
            NgProxy = request.meta['proxy']
            self.invalid_proxy.add(NgProxy)
        self.proxy = Proxy().get_proxy()
        request.dont_filter = True
        # logger.info('代理中间件异常模块，异常为{} '.format(exception))
        logger.info('代理中间件异常模块，异常为{}，新的代理为 {}'.format(exception, self.proxy))
        if exception in [ConnectionRefusedError, TimeoutError]:
            logger.info(exception)


class MyRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # logger.info('重试中间件返回值异常, 进行重试..............')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
            # logger.info('重试中间件连接异常,异常类型为{},加入重试队列.............'.format(exception))
            self.pre_url = str(request)
            return self._retry(request, exception, spider)
