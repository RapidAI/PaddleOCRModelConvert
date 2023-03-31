# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
# github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/ppocr/utils/network.py
import re
import tarfile
from pathlib import Path
from typing import Union

import requests
from tqdm import tqdm


class DownloadModelError(Exception):
    pass


def mkdir(dir_path: Union[str, Path]):
    """创建目录

    Args:
        dir_path (Union[str, Path]): 路径地址
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def download_file(url: str, save_dir: str) -> Path:
    """下载指定url的文件

    Args:
        url (str): 文件url路径
        save_dir (str): 下载保存的目录

    Raises:
        DownloadModelError: 下载异常

    Returns:
        Path: 下载到本地的文件全路径
    """
    mkdir(save_dir)

    response = requests.get(url, stream=True, timeout=(120, 120))
    status_code = response.status_code

    if status_code != 200:
        raise DownloadModelError('Something went wrong while downloading models')

    total_size_in_bytes = int(response.headers.get('content-length', 1))
    block_size = 1024  # 1 Kibibyte

    save_path = Path(save_dir) / Path(url).name
    with tqdm(total=total_size_in_bytes, unit='iB',
              unit_scale=True, desc='Downloading') as pb:
        with open(save_path, 'wb') as file:
            for data in response.iter_content(block_size):
                pb.update(len(data))
                file.write(data)
    return save_path


def unzip_file(file_path: str, save_dir: str, is_del_raw=True) -> Path:
    """解压下载得到的tar模型文件，会自动解压到 :code:`save_dir` 下以 :code:`file_path` 命名的目录下

    Args:
        file_path (str): tar格式文件路径
        save_dir (str): 解压路径
        is_del_raw (bool, optional): 是否删除原文件. Defaults to True.

    Returns:
        Path: 解压后模型保存路径
    """
    model_dir = Path(save_dir) / Path(file_path).stem
    mkdir(model_dir)

    tar_file_name_list = ['.pdiparams', '.pdiparams.info', '.pdmodel']
    with tarfile.open(file_path, 'r') as tarObj:
        for member in tarObj.getmembers():
            filename = None

            for tar_file_name in tar_file_name_list:
                if member.name.endswith(tar_file_name):
                    filename = 'inference' + tar_file_name

            if filename is None:
                continue

            save_file_path = model_dir / filename
            file = tarObj.extractfile(member)
            with open(save_file_path, 'wb') as f:
                f.write(file.read())
    if is_del_raw:
        Path(file_path).unlink()
        print(f'The {file_path} has been deleted.')
    return model_dir


def is_http_url(s: Union[str, Path]) -> bool:
    """判断是否为url

    Args:
        s (Union[str, Path]): 输入的字符串

    Returns:
        bool: 是或否
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if regex.match(str(s)):
        return True
    return False
