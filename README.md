# singutools
本仓库为轻量级的 Python3 代码工具包，实现部分常用功能，可以方便快捷的构建 Python 程序。现已包含环境检测、系统命令和爬虫的通用代码。

## 依赖 Python 第三方类库
`requests` >= 2.22.0
`BeautifulSoup` >= 4.7.1

## spider.py（爬虫工具包）
该模块为爬虫程序提供了 `requests + BeautifulSoup` 的快速实现，并提供了异常重试、延迟等待、文件下载等常用的爬虫功能。
