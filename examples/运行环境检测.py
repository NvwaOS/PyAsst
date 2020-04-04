from src import env


def main():
    results = {
        '操作系统': None,
        '系统架构': None,
        '语言环境': None,
        'Python版本': None
    }
    # 判断操作系统类型
    if env.isWindows():
        results['操作系统'] = 'Windows'
    elif env.isMacOS():
        results['操作系统'] = 'MacOS'
    elif env.isLinux():
        results['操作系统'] = 'Linux'
    else:
        results['操作系统'] = '未知操作系统'

    # 判断系统架构
    if env.is32Bit():
        results['系统架构'] = '32位'
    elif env.is64Bit():
        results['系统架构'] = '64位'
    else:
        results['系统架构'] = '未知系统架构'

    # 判断语言环境
    if env.isChinese():
        results['语言环境'] = '中文版'
    elif env.isEnglish():
        results['语言环境'] = '英文版'
    else:
        results['语言环境'] = '未知语言环境'

    # 判断 Python 解释器版本
    if env.isPython3():
        results['Python版本'] = 'Python 3.x'
    elif env.isPython2():
        results['Python版本'] = 'Python 2.x'
    else:
        results['Python版本'] = '未知版本'

    print('当前运行的操作系统是：{操作系统} {系统架构} {语言环境}，Python解释器版本是：{Python版本}'.format(**results))


if __name__ == '__main__':
    main()
