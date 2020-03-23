import os
import sys
import json
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    from src.spider import Delay, RequestHandler

    proxy_pool = list()
    # 创建请求处理器
    handler = RequestHandler(
        # 设置 HTTP 请求头
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36'
        },
        # 设置异常重试次数
        retry=3,
        # 设置延迟
        # 每请求 2 次，延迟 1 秒
        delay=Delay(step=2, sleep=1)
    )
    for page in range(10):
        # 通过请求处理器发起网络请求，并返回 HTML 文本
        html = handler.html('https://www.kuaidaili.com/free/inha/{}/'.format(page))
        soup = BeautifulSoup(html, 'lxml')
        servers = soup.select('#list > table > tbody > tr')
        for server in servers:
            ip = server.select_one('td:nth-child(1)').text
            post = server.select_one('td:nth-child(2)').text
            protocol = server.select_one('td:nth-child(4)').text
            proxy_pool.append({
                'ip': ip,
                'post': post,
                'protocol': protocol
            })
    with open('ProxyPool.json', 'w') as f:
        json.dump(proxy_pool, f)


if __name__ == '__main__':
    main()
