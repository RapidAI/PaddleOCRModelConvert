# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import hashlib
import shutil
import sys
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from paddleocr_convert import PaddleOCRModelConvert, download_file


def get_md5(filename):
    with open(filename, "rb") as file_txt:
        myhash = hashlib.md5(file_txt.read())
    return myhash.hexdigest()


def is_windows():
    if sys.platform.startswith("win"):
        return True
    return False


converter = PaddleOCRModelConvert()
save_dir = cur_dir / "models"


def test_url_input():
    url = "https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar"
    onnx_path = converter(url, save_dir, is_del_raw=True)
    md5_value = get_md5(onnx_path)
    if is_windows():
        assert md5_value == "877a502cf1c4817e8eb50d847f35dd6f"
    else:
        assert md5_value == "67ffba91f570b15f15ef2b9da9505e0b"
    shutil.rmtree(save_dir)


def test_local_input():
    url = "https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar"
    tar_path = download_file(url, save_dir)
    onnx_path = converter(tar_path, save_dir, is_del_raw=True)

    md5_value = get_md5(onnx_path)
    if is_windows():
        assert md5_value == "877a502cf1c4817e8eb50d847f35dd6f"
    else:
        assert md5_value == "67ffba91f570b15f15ef2b9da9505e0b"

    shutil.rmtree(save_dir)


def test_rec_input():
    url = "https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar"
    txt_url = "https://gitee.com/paddlepaddle/PaddleOCR/raw/release/2.6/ppocr/utils/ppocr_keys_v1.txt"
    onnx_path = converter(url, save_dir, txt_path=txt_url, is_del_raw=True)
    md5_value = get_md5(onnx_path)

    if is_windows():
        assert md5_value == "e40e359fd082498ed30abf80223e8e05"
    else:
        assert md5_value == "0ba3af0828db6faa400612cf1b000965"
    shutil.rmtree(save_dir)


def test_rec_input_local():
    url = "https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar"
    txt_url = "https://gitee.com/paddlepaddle/PaddleOCR/raw/release/2.6/ppocr/utils/ppocr_keys_v1.txt"
    tar_path = download_file(url, save_dir)
    txt_path = download_file(txt_url, save_dir)

    onnx_path = converter(tar_path, save_dir, txt_path=txt_path, is_del_raw=True)
    md5_value = get_md5(onnx_path)

    if is_windows():
        assert md5_value == "e40e359fd082498ed30abf80223e8e05"
    else:
        assert md5_value == "0ba3af0828db6faa400612cf1b000965"

    shutil.rmtree(save_dir)
