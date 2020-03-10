import os
from . import env

PAUSE = {
    'windows': 'PAUSE',
    'macos': None
}

CLEAR = {
    'windows': 'CLS',
    'macos': 'clear'
}


def _select_cmd_(commands: dict) -> str:
    if env.isWindows():
        return commands['windows']
    elif env.isMacOS():
        return commands['macos']
    elif env.isLinux():
        return commands['linux']
    elif env.isUnix():
        return commands['unix']
    raise RuntimeError('未知系统版本')


def _exec_command_(commands: dict) -> bool:
    cmd = _select_cmd_(commands)
    if cmd is not None:
        os.system(cmd)
        return True
    return False


def pause():
    if not _exec_command_(PAUSE):
        input('请按任意键继续...')


def clear():
    if not _exec_command_(CLEAR):
        print('\n' * 100)
