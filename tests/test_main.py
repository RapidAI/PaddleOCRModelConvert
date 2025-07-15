# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import hashlib
import shutil
import sys
from pathlib import Path

import pytest

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from paddleocr_convert import PaddleOCRModelConvert, download_file
from paddleocr_convert.utils import mkdir

converter = PaddleOCRModelConvert()


@pytest.fixture
def setup_and_teardonw():
    save_dir = cur_dir / "models"
    mkdir(save_dir)

    yield save_dir

    shutil.rmtree(save_dir)


def get_md5(filename):
    with open(filename, "rb") as file_txt:
        myhash = hashlib.md5(file_txt.read())
    return myhash.hexdigest()


def is_windows():
    if sys.platform.startswith("win"):
        return True
    return False


def test_ppocrv5(setup_and_teardonw):
    save_dir = setup_and_teardonw
    url = "https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-OCRv5_mobile_det_infer.tar"
    onnx_path = converter(url, save_dir, is_del_raw=False)
    assert Path(onnx_path).exists()


def test_url_input(setup_and_teardonw):
    save_dir = setup_and_teardonw
    url = "https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar"
    onnx_path = converter(url, save_dir, is_del_raw=True)
    assert Path(onnx_path).exists()


def test_local_input(setup_and_teardonw):
    save_dir = setup_and_teardonw
    url = "https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar"
    tar_path = download_file(url, save_dir)
    onnx_path = converter(tar_path, save_dir, is_del_raw=True)

    assert Path(onnx_path).exists()


def test_rec_input(setup_and_teardonw):
    save_dir = setup_and_teardonw
    url = "https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar"
    txt_url = "https://gitee.com/paddlepaddle/PaddleOCR/raw/release/2.6/ppocr/utils/ppocr_keys_v1.txt"
    onnx_path = converter(url, save_dir, txt_path=txt_url, is_del_raw=True)

    assert Path(onnx_path).exists()


def test_rec_input_local(setup_and_teardonw):
    save_dir = setup_and_teardonw
    url = "https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar"
    txt_url = "https://gitee.com/paddlepaddle/PaddleOCR/raw/release/2.6/ppocr/utils/ppocr_keys_v1.txt"
    tar_path = download_file(url, save_dir)
    txt_path = download_file(txt_url, save_dir)

    onnx_path = converter(tar_path, save_dir, txt_path=txt_path, is_del_raw=True)

    assert Path(onnx_path).exists()
