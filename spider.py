import os
import json
import time
import logging
import requests
from typing import Union, Optional


CHUCK_SIZE = 8192
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.130 Safari/537.36 '
}


class Delay:
    def __init__(self, step: int = 10, sleep: float = 1):
        self.counter = 0
        self.step = step
        self.sleep = sleep

    def action(self):
        self.counter += 1
        if self.counter % self.step == 0:
            time.sleep(self.sleep)


class RequestHandler:
    """
    请求处理器
    """
    @staticmethod
    def _makedirs_(path):
        dir_path, filename = os.path.split(path)
        dir_path = os.path.abspath(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @classmethod
    def decode(cls, content, encodes, encoding):
        for code in encodes:
            if code is None:
                continue
            try:
                return content.decode(code)
            except UnicodeDecodeError:
                pass
        if encoding is not None:
            return content.decode(encoding, errors='ignore')
        raise RuntimeError('无法确定内容的编码格式，已尝试的编码格式有: %s' % list(filter(bool, encodes)), content)

    class _FalseDelay_(Delay):
        """
        假延迟
        """
        def action(self):
            pass

    def __init__(self, session: bool = True, headers: dict = None, encoding: Union[str, list, tuple] = 'UTF-8',
                 retry: int = 3, delay: Optional[Delay] = None, **kwargs):
        """
        请求处理器
        :param session:  是否启用 Session 会话
        如若启用，则该请求处理器的所有请求都将采用同一个会话
        :param headers:  HTTP请求头
        :param encoding: 字符编码，默认为 UTF-8
        该项可以提供多个字符编码，请求处理器会从前到后逐渐尝试解密，直到正确解码或所有的编码都无法正确解析
        :param retry:    失败重试次数，默认为 3 次
        :param delay:    请求延迟，默认为不延迟
        请求处理器运行创建一个延迟对象，每次发起请求时会激活延迟对象，是否进行延迟有延迟对象进行处理
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.logger = logging.getLogger(__name__)

        self.session = requests.Session() if session else requests

        self.methods = {
            'get': self.session.get,
            'post': self.session.post
        }

        if headers is None:
            headers = HEADERS.copy()
        self.headers = headers

        if type(encoding) == str:
            encoding = (encoding,)
        elif type(encoding) == list:
            encoding = tuple(encoding)
        self.encodes: tuple = encoding

        self.retry = retry

        if delay is None:
            delay = self._FalseDelay_()
        self.delay = delay

    def request(self, url: str, method: str, **kwargs) -> requests.Response:
        if not method or not url:
            raise RuntimeError('参数不完整')
        _method = self.methods.get(method)
        if _method is None:
            raise RuntimeError('未知的 HTTP 请求方式：' + method)

        # 请求响应结果
        res = None
        # 当前重试次数
        retry_count = 0

        # 如果当前重试次数大于或等于设定的最大重试次数，则跳出循环
        # 首次请求也计算在内
        while retry_count < self.retry:
            # 发起请求之前，优先累加重试次数
            retry_count += 1
            # 激活延迟处理器，每次重试也要计入延迟
            self.delay.action()
            # 发起请求
            res = _method(url, headers=self.headers, **kwargs)
            if res.status_code != 200:
                # 响应状态码不为 200，则发起重试
                continue
            return res
        # 超过最大重试次数，则抛出异常
        raise RuntimeError('「HTTP异常」状态码：%d，请求地址：%s' % (res.status_code, url))

    def get(self, url: str) -> requests.Response:
        return self.request(url, 'get')

    def post(self, url: str) -> requests.Response:
        return self.request(url, 'post')

    def html(self, url: str, encoding: Optional[str] = None, uncomment: bool = False) -> str:
        res = self.request(url, 'get')
        html = self.decode(res.content, self.encodes, encoding)
        if uncomment:
            html = html.replace('<!--', '').replace('-->', '')
        return html

    def json(self, url: str, method: str = 'get', encoding: Optional[str] = None) -> Union[list, dict]:
        res = self.request(url, method)
        content = self.decode(res.content, self.encodes, encoding)
        return json.loads(content)

    def download(self, url: str, save_path: str, method: str = 'get'):
        # 如果文件夹不存在，则创建
        self._makedirs_(save_path)
        with open(save_path, 'wb') as f:
            with self.request(url, method, stream=True) as res:
                if 'Content-Length' in res.headers:
                    content_length = int(res.headers['Content-Length'])
                    download_length = 0
                    for chuck in res.iter_content(CHUCK_SIZE):
                        if chuck:
                            f.write(chuck)
                        download_length += len(chuck)
                        if download_length >= content_length:
                            break
                else:
                    f.write(res.content)
