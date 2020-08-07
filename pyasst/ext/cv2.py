import os
from pathlib import Path
from typing import Any, Union, IO
from ..common import ModuleIsNotInstallError, FileSystemUtil

try:
    import cv2 as cv
except ModuleNotFoundError as E:
    raise ModuleIsNotInstallError('OpenCV', 'pip install opencv-python') from E

try:
    import numpy as np
except ModuleNotFoundError as E:
    raise ModuleIsNotInstallError('Numpy', 'pip install numpy') from E


def imread(file: Union[IO, str, Path], flags: int = cv.IMREAD_ANYCOLOR) -> Union[None, np.ndarray]:
    """
    Support imread of Chinese path.
    支持中文路径的 imread。

    :param file: file or str or Path
    :param flags: The same flags as in cv::imread, see cv::ImreadModes.
    :return: Image
    """
    return cv.imdecode(np.fromfile(file, dtype=np.uint8), flags)


def imwrite(file: Union[IO, str, Path], img: np.ndarray, params: Any = None):
    """
    Support imwrite of Chinese path.
    支持中文路径的 imwrite。

    :param file: file or str or Path
    :param img: Image to be written.
    :param params: Format-specific parameters. See cv::imwrite and cv::ImwriteFlags.
    :return:
    """
    dirpath, name, ext = FileSystemUtil.split(file)
    FileSystemUtil.make_if_doesnt_exist(dirpath)
    if not ext:
        ext = '.png'
    filepath = os.path.join(dirpath, name + ext)
    cv.imencode(ext, img, params)[1].tofile(filepath)
