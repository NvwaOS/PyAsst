

class StringUtil:
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
        raise RuntimeError('无法确定内容的编码格式，已尝试的编码格式有: %s' % list(filter(bool, encodes)))

