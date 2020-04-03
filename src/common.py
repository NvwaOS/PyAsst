import os


class StringUtil:
    @classmethod
    def decode(cls, content: bytes, encodes: str, encoding: str) -> str:
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
