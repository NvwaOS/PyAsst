from bs4 import BeautifulSoup
from pyasst.spider import Delay, RequestHandler

MAIN_URL = 'http://www.biquge.tv'


def get_chapter_list(handler, book_id):
    chapter_list = list()
    html = handler.html('{}/{}/'.format(MAIN_URL, book_id))
    soup = BeautifulSoup(html, 'lxml')
    chapters = soup.select('#list > dl > dd > a')
    for chapter in chapters:
        chapter_list.append({
            'name': chapter.text,
            'url': '{}{}'.format(MAIN_URL, chapter.attrs['href'])
        })
    return chapter_list


def get_content(handler, chapter):
    html = handler.html(chapter['url'])
    soup = BeautifulSoup(html, 'lxml')
    content = soup.select_one('#content')
    return content.text


def main():
    # 创建请求处理器
    handler = RequestHandler(
        # 设置 HTTP 请求头
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36'
        },
        # 尝试使用 GBK 或 UTF-8 编码方式
        encoding=('GBK', 'UTF-8'),
        # 设置异常重试次数
        retry=3,
        # 设置延迟
        # 每请求 2 次，延迟 1 秒
        delay=Delay(step=2, sleep=1)
    )
    chapter_list = get_chapter_list(handler, '25_25228')
    with open('book.txt', 'w', encoding='UTF-8') as f:
        for chapter in chapter_list:
            content = get_content(handler, chapter)
            f.write('\t%s\n\n' % chapter['name'])
            f.write(content)
            f.write('\n\n')


if __name__ == '__main__':
    main()
