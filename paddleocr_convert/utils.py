# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
# github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/ppocr/utils/network.py
import tarfile
from pathlib import Path

import requests
from tqdm import tqdm


def mkdir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def download_file(url: str, save_dir: str) -> Path:
    mkdir(save_dir)

    response = requests.get(url, stream=True)
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
    """解压下载得到的tar模型文件，会自动解压到save_dir下以file_path命名的目录下

    Args:
        file_path (str): _description_
        save_dir (str): _description_
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
    return model_dir


class DownloadModelError(Exception):
    pass
