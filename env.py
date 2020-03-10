#!/usr/bin/env python
# -- coding: UTF-8 -*-
# Author : Singu
# Email : singu@singu.top
# Date : 2019-01-25

"""
This module has the following module variables:
该模块具有以下模块变量:

    PYTHON_VERSION:
        Python interpreter variable, which is a tuple type (major_version, minor_version, micro_version)
        Python解释器变量, 它是元组类型 (主版本号, 次版本号, 微版本号)

    SYSTEM:
        Operating system version variable, which is a tuple type (operating_system_type, release_version)
        操作系统版本变量, 它是一种元组类型 (操作系统类型，发行版本)

    SYSTEM_DETAILED:
        Operating system detail variable, which is a tuple type that determines elements based on the specific system
        操作系统详细信息变量, 它是一种基于特定系统确定元素的元组类型

    HOSTNAME:
        Host name of this machine
        本机的主机名

    ARCHITECTURE:
        System architecture type, 64-bit or 32-bit
        系统架构类型, 64位 或 32位

    SYSTEM_LANGUAGE:
        System language
        系统语言类型

    SYSTEM_ENCODING:
        System encoding
        系统编码方式

    DEFAULT_ENCODING:
        Default encoding
        默认编码方式
"""

import sys
import platform
import locale

'''
PYTHON_VERSION:
    Python interpreter variable, which is a tuple type (major_version, minor_version, micro_version)
    Python解释器变量, 它是元组类型 (主版本号, 次版本号, 微版本号)
'''
PYTHON_VERSION = tuple(map(int, platform.python_version_tuple()))


def isPython2():
    """
    Determine if the current version of the Python interpreter is 2.x
    判断Python解释器的当前版本是否为 2.x
    """
    return PYTHON_VERSION[0] == 2


def isPython3():
    """
    Determine if the current version of the Python interpreter is 3.x
    判断Python解释器的当前版本是否为 3.x
    """
    return PYTHON_VERSION[0] == 3


'''
SYSTEM:
    Operating system version variable, which is a tuple type (operating_system_type, release_version)
    操作系统版本变量, 它是一种元组类型 (操作系统类型，发行版本)
'''
SYSTEM = (platform.system(), platform.release())


def isWindows():
    """
    Determine if the current operating system is Windows
    确定当前操作系统是否为 Windows
    """
    return SYSTEM[0] == 'Windows'


def isLinux():
    """
    Determine if the current operating system is Linux
    确定当前操作系统是否为 Linux
    """
    return SYSTEM[0] == 'Linux'


def isMacOS():
    """
    Determine if the current operating system is MacOS
    确定当前操作系统是否为 MacOS
    """
    return SYSTEM[0] == 'Darwin'


def isUnix():
    """
    Determine whether the current operating system is a Unix architecture
    确定当前的操作系统是否是 Unix 体系结构
    """
    return isMacOS() or isLinux()


'''
SYSTEM_DETAILED:
    Operating system detail variable, which is a tuple type that determines elements based on the specific system
    操作系统详细信息变量, 它是一种基于特定系统确定元素的元组类型
'''
SYSTEM_DETAILED = ()
if isWindows():
    SYSTEM_DETAILED = platform.win32_ver()
elif isLinux():
    SYSTEM_DETAILED = platform.linux_distribution()
elif isMacOS():
    SYSTEM_DETAILED = platform.mac_ver()

'''
HOSTNAME:
    Host name of this machine
    本机的主机名
'''
HOSTNAME = platform.node()

'''
ARCHITECTURE:
    System architecture type, 64-bit or 32-bit
    系统架构类型, 64位 或 32位
'''
ARCHITECTURE = platform.architecture()[0]


def is64Bit():
    """
    Determine whether the current operating system is a 64-bit architecture
    确定当前操作系统是否为 64 位体系结构
    """
    return ARCHITECTURE == '64bit'


def is32Bit():
    """
    Determine whether the current operating system is a 32-bit architecture
    确定当前操作系统是否为 32 位体系结构
    """
    return ARCHITECTURE == '32bit'


SYSTEM_AREA = locale.getdefaultlocale()

'''
SYSTEM_LANGUAGE:
    System language
    系统语言类型
'''
SYSTEM_LANGUAGE = SYSTEM_AREA[0]

'''
SYSTEM_ENCODING:
    System encoding
    系统编码方式
'''
SYSTEM_ENCODING = SYSTEM_AREA[1]

'''
DEFAULT_ENCODING:
    Default encoding
    默认编码方式
'''
DEFAULT_ENCODING = sys.getdefaultencoding()


def isChinese():
    """
    Determine whether the current system language is Chinese
    确定当前系统语言是否为 中文
    """
    return SYSTEM_LANGUAGE == 'zh_CN'


def isEnglish():
    """
    Determine whether the current system language is English
    确定当前系统语言是否为 英文
    """
    return SYSTEM_LANGUAGE == 'en_US'


__all__ = [
    'PYTHON_VERSION', 'SYSTEM',
    'SYSTEM_DETAILED', 'HOSTNAME',
    'ARCHITECTURE', 'SYSTEM_LANGUAGE',
    'SYSTEM_ENCODING', 'DEFAULT_ENCODING',
    'isPython2', 'isPython3',
    'isWindows', 'isLinux',
    'isMacOS', 'isUnix',
    'is64Bit', 'is32Bit',
    'isChinese', 'isEnglish'
]
