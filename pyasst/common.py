import os
from . import env
from typing import Union


class ModuleIsNotInstallError(RuntimeError):
    def __init__(self, module: str, command: str = None):
        self.module_name = module
        self.command = command if command is not None else f'pip install {module}'

    def __str__(self):
        return (
            '您需要先安装 {module} 框架，使用 "{command}" 命令。'
            if env.isChinese() else
            'You need to install {module} module first, use "{command}" command.'
        ).format(module=self.module_name, command=self.command)


class StringUtil:
    @classmethod
    def decode(cls, content: bytes, encodes: Union[str, list, tuple], encoding: str) -> str:
        for code in encodes:
            if code is None:
                continue
            try:
                return content.decode(code)
            except UnicodeDecodeError:
                pass
        if encoding is not None:
            return content.decode(encoding, errors='ignore')
        raise RuntimeError('无法确定内容的编码格式，已尝试的编码格式有: %s' % list(filter(bool, encodes)))


class FileSystemUtil:
    @classmethod
    def split(cls, filepath: str) -> (str, str, str):
        dirpath, filename = os.path.split(filepath)
        name, ext = os.path.splitext(filename)
        return dirpath, name, ext

    @classmethod
    def make_if_doesnt_exist(cls, path: str) -> None:
        if not path:
            return
        path = os.path.abspath(path)
        if not os.path.exists(path):
            os.makedirs(path)
