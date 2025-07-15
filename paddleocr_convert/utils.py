# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
# github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/ppocr/utils/network.py
import logging
import tarfile
from pathlib import Path
from typing import List, Set, TypedDict, Union
from urllib.parse import urlparse

import colorlog
import requests
from tqdm import tqdm

InputType = Union[str, Path]


class Logger:
    def __init__(self, log_level=logging.DEBUG, logger_name=None):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.logger.propagate = False

        formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(levelname)s] %(asctime)s [PaddleOCRModelConvert] %(filename)s:%(lineno)d: %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )

        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)

            console_handler.setLevel(log_level)
            self.logger.addHandler(console_handler)

    def get_log(self):
        return self.logger


def read_txt(txt_path: Union[str, Path]) -> str:
    with open(str(txt_path), "r", -1, "u8") as f:
        value = f.read()
    return value


def is_contain(sentence: str, key_words: Union[str, List]) -> bool:
    """sentences中是否包含key_words中任意一个"""
    return any(i in sentence for i in key_words)


class UnzipResult(TypedDict):
    model_dir: Path
    my_files: Set[str]


class DownloadModelError(Exception):
    pass


def mkdir(dir_path: InputType):
    """创建目录

    Args:
        dir_path (Union[str, Path]): 路径地址
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def download_file(url: str, save_dir: InputType) -> Path:
    """下载指定url的文件

    Args:
        url (str): 文件url路径
        save_dir (InputType): 下载保存的目录

    Raises:
        DownloadModelError: 下载异常

    Returns:
        Path: 下载到本地的文件全路径
    """
    mkdir(save_dir)

    response = requests.get(url, stream=True, timeout=(120, 120))
    status_code = response.status_code

    if status_code != 200:
        raise DownloadModelError("Something went wrong while downloading models")

    total_size_in_bytes = int(response.headers.get("content-length", 1))
    block_size = 1024  # 1 Kibibyte

    save_path = Path(save_dir) / Path(url).name
    with tqdm(
        total=total_size_in_bytes, unit="iB", unit_scale=True, desc="Downloading"
    ) as pb:
        with open(save_path, "wb") as file:
            for data in response.iter_content(block_size):
                pb.update(len(data))
                file.write(data)
    return save_path


def unzip_file(
    file_path: str, save_dir: InputType, is_del_raw: bool = True
) -> UnzipResult:
    """解压下载得到的tar模型文件，会自动解压到save_dir下以file_path命名的目录下

    Args:
        file_path (str): tar格式文件路径
        save_dir (InputType): 解压路径
        is_del_raw (bool, optional): 是否删除原文件. Defaults to True.

    Returns:
        dict:
            - model_dir (Path): 解压后模型保存路径
            - my_files (set): 解压得到的文件名集合
    """
    model_dir = Path(save_dir) / Path(file_path).stem
    mkdir(model_dir)

    tar_file_name_list = [".pdiparams", ".pdiparams.info", ".pdmodel", ".json"]
    my_files = set()
    with tarfile.open(file_path, "r") as tarObj:
        for member in tarObj.getmembers():
            filename = None

            for tar_file_name in tar_file_name_list:
                if member.name.endswith(tar_file_name):
                    filename = "inference" + tar_file_name
                    my_files.add(filename)

            if filename is None:
                continue

            save_file_path = model_dir / filename
            file = tarObj.extractfile(member)
            with open(save_file_path, "wb") as f:
                f.write(file.read())
    if is_del_raw:
        Path(file_path).unlink()
        print(f"The {file_path} has been deleted.")
    return {"model_dir": model_dir, "my_files": my_files}


def is_http_url(s: InputType) -> bool:
    try:
        result = urlparse(str(s))
        return all([result.scheme, result.netloc])
    except Exception as e:
        return False
