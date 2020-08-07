import os
from typing import Any, Union
from .common import FileSystemUtil


def __none_function__(*argv, **kwargs) -> None:
    raise Exception("相关第三方包未安装，所以该函数未实现。")


# 增加 OpenCV 功能拓展
cv_imread = __none_function__
cv_imwrite = __none_function__
try:
    import cv2 as cv
    import numpy as np

    def cv_imread(filename: Any, flags: Any = cv.IMREAD_ANYCOLOR) -> Union[None, np.ndarray]:
        return cv.imdecode(np.fromfile(filename, dtype=np.uint8), flags)

    def cv_imwrite(filename: Any, img: Any, params: Any = None):
        dirpath, name, ext = FileSystemUtil.split(filename)
        FileSystemUtil.make_if_doesnt_exist(dirpath)
        if not ext:
            ext = '.png'
        filepath = os.path.join(dirpath, name + ext)
        cv.imencode(ext, img, params)[1].tofile(filepath)
except ModuleNotFoundError:
    pass
